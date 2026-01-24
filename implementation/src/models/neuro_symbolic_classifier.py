"""
Neuro-symbolic hybrid model implementation.

This module implements a neuro-symbolic approach that combines
neural network learning with symbolic reasoning to address
common sense gaps and improve explainability.
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Union, Optional
import logging

from ..base import BaseModel, BaseExplainer, BaseReasoner

logger = logging.getLogger(__name__)


class NeuroSymbolicClassifier(BaseModel):
    """
    Neuro-symbolic classifier that combines neural networks with symbolic reasoning.
    
    This model addresses limitations in common sense and explainability by:
    1. Integrating symbolic knowledge into neural representations
    2. Providing interpretable reasoning paths
    3. Supporting both statistical and logical inference
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize neuro-symbolic classifier.
        
        Args:
            config: Model configuration containing:
                - input_size: Size of input features
                - hidden_layers: List of hidden layer sizes
                - num_classes: Number of output classes
                - symbolic_rules: List of symbolic rules
                - reasoning_engine: Type of reasoning engine
                - integration_method: Method for integrating neural and symbolic components
        """
        super().__init__(config)
        
        self.input_size = config.get('input_size')
        self.hidden_layers = config.get('hidden_layers', [256, 128, 64])
        self.num_classes = config.get('num_classes')
        self.symbolic_rules = config.get('symbolic_rules', [])
        self.reasoning_engine = config.get('reasoning_engine', 'prolog')
        self.integration_method = config.get('integration_method', 'late_fusion')
        
        # Initialize neural network component
        self._build_neural_network()
        
        # Initialize symbolic reasoning component
        self._build_symbolic_reasoner()
        
        # Initialize integration layer
        self._build_integration_layer()
        
        logger.info(f"Initialized NeuroSymbolicClassifier with {self.num_classes} classes")
    
    def _build_neural_network(self):
        """Build the neural network component."""
        layers = []
        
        # Input layer
        layers.append(nn.Linear(self.input_size, self.hidden_layers[0]))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(0.2))
        
        # Hidden layers
        for i in range(len(self.hidden_layers) - 1):
            layers.append(nn.Linear(self.hidden_layers[i], self.hidden_layers[i + 1]))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
        
        # Output layer (before integration)
        layers.append(nn.Linear(self.hidden_layers[-1], self.hidden_layers[-1]))
        layers.append(nn.ReLU())
        
        self.neural_network = nn.Sequential(*layers)
        
    def _build_symbolic_reasoner(self):
        """Build the symbolic reasoning component."""
        self.symbolic_reasoner = SimpleReasoner(
            rules=self.symbolic_rules,
            engine=self.reasoning_engine
        )
    
    def _build_integration_layer(self):
        """Build the integration layer for combining neural and symbolic outputs."""
        if self.integration_method == 'late_fusion':
            self.integration_layer = nn.Sequential(
                nn.Linear(self.hidden_layers[-1] + self.symbolic_reasoner.get_output_size(), 128),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, self.num_classes)
            )
        elif self.integration_method == 'attention_fusion':
            self.integration_layer = AttentionFusion(
                neural_size=self.hidden_layers[-1],
                symbolic_size=self.symbolic_reasoner.get_output_size(),
                num_classes=self.num_classes
            )
        else:
            raise ValueError(f"Unknown integration method: {self.integration_method}")
    
    def fit(self, X: Union[np.ndarray, pd.DataFrame], 
            y: Union[np.ndarray, pd.DataFrame]) -> 'NeuroSymbolicClassifier':
        """Train the neuro-symbolic model.
        
        Args:
            X: Training features
            y: Training targets
            
        Returns:
            Self for method chaining
        """
        logger.info("Training NeuroSymbolicClassifier...")
        
        # Convert to torch tensors
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, (pd.DataFrame, pd.Series)):
            y = y.values
            
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.LongTensor(y)
        
        # Training parameters
        learning_rate = self.config.get('learning_rate', 0.001)
        epochs = self.config.get('epochs', 100)
        batch_size = self.config.get('batch_size', 32)
        
        # Initialize optimizer and loss function
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        criterion = nn.CrossEntropyLoss()
        
        # Training loop
        dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        self.train()
        for epoch in range(epochs):
            total_loss = 0.0
            for batch_X, batch_y in dataloader:
                optimizer.zero_grad()
                
                # Forward pass
                outputs = self._forward_pass(batch_X)
                loss = criterion(outputs, batch_y)
                
                # Backward pass
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            if (epoch + 1) % 10 == 0:
                logger.info(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
        
        self.is_trained = True
        logger.info("Training completed successfully.")
        return self
    
    def _forward_pass(self, X: torch.Tensor) -> torch.Tensor:
        """Forward pass through the model.
        
        Args:
            X: Input tensor
            
        Returns:
            Output tensor
        """
        # Neural network forward pass
        neural_features = self.neural_network(X)
        
        # Symbolic reasoning
        symbolic_outputs = []
        for i in range(X.size(0)):
            symbolic_output = self.symbolic_reasoner.reason(
                facts=[{"features": X[i].detach().cpu().numpy()}],
                query="classify"
            )
            symbolic_outputs.append(symbolic_output.get("features", torch.zeros(self.symbolic_reasoner.get_output_size())))
        
        symbolic_tensor = torch.stack(symbolic_outputs)
        
        # Integration
        if self.integration_method == 'late_fusion':
            combined_features = torch.cat([neural_features, symbolic_tensor], dim=1)
            outputs = self.integration_layer(combined_features)
        elif self.integration_method == 'attention_fusion':
            outputs = self.integration_layer(neural_features, symbolic_tensor)
        
        return outputs
    
    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Make predictions on new data.
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        self.eval()
        with torch.no_grad():
            if isinstance(X, pd.DataFrame):
                X = X.values
            
            X_tensor = torch.FloatTensor(X)
            outputs = self._forward_pass(X_tensor)
            predictions = torch.argmax(outputs, dim=1).detach().cpu().numpy()
        
        return predictions
    
    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Predict class probabilities.
        
        Args:
            X: Input features
            
        Returns:
            Class probabilities
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        self.eval()
        with torch.no_grad():
            if isinstance(X, pd.DataFrame):
                X = X.values
            
            X_tensor = torch.FloatTensor(X)
            outputs = self._forward_pass(X_tensor)
            probabilities = torch.softmax(outputs, dim=1).detach().cpu().numpy()
        
        return probabilities
    
    def explain(self, X: Union[np.ndarray, pd.DataFrame]) -> Dict[str, Any]:
        """Provide explanation for predictions.
        
        Args:
            X: Input features to explain
            
        Returns:
            Explanation dictionary containing:
                - neural_importance: Feature importance from neural component
                - symbolic_reasoning: Symbolic reasoning steps
                - integrated_explanation: Combined explanation
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before providing explanations")
        
        # Get neural feature importance
        neural_importance = self._get_neural_importance(X)
        
        # Get symbolic reasoning
        symbolic_reasoning = self._get_symbolic_reasoning(X)
        
        # Combine explanations
        integrated_explanation = self._combine_explanations(
            neural_importance, symbolic_reasoning
        )
        
        return {
            "neural_importance": neural_importance,
            "symbolic_reasoning": symbolic_reasoning,
            "integrated_explanation": integrated_explanation
        }
    
    def _get_neural_importance(self, X: Union[np.ndarray, pd.DataFrame]) -> Dict[str, Any]:
        """Get feature importance from neural component."""
        # Simplified feature importance using gradient-based method
        if isinstance(X, pd.DataFrame):
            X_values = X.values
            feature_names = X.columns.tolist()
        else:
            X_values = X
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        self.eval()
        X_tensor = torch.FloatTensor(X_values)
        X_tensor.requires_grad_(True)
        
        outputs = self.neural_network(X_tensor)
        loss = torch.sum(outputs)
        loss.backward()
        
        gradients = X_tensor.grad.detach().cpu().numpy()
        importance_scores = np.mean(np.abs(gradients), axis=0)
        
        return {
            "method": "gradient_importance",
            "feature_names": feature_names,
            "importance_scores": importance_scores.tolist(),
            "most_important": feature_names[np.argmax(importance_scores)]
        }
    
    def _get_symbolic_reasoning(self, X: Union[np.ndarray, pd.DataFrame]) -> Dict[str, Any]:
        """Get symbolic reasoning explanation."""
        if isinstance(X, pd.DataFrame):
            X_values = X.values
        else:
            X_values = X
        
        # Get reasoning for first instance (for demonstration)
        reasoning_result = self.symbolic_reasoner.reason(
            facts=[{"features": X_values[0]}],
            query="explain_classification"
        )
        
        return {
            "method": "symbolic_rules",
            "rules_applied": reasoning_result.get("rules_applied", []),
            "reasoning_steps": reasoning_result.get("steps", []),
            "confidence": reasoning_result.get("confidence", 0.0)
        }
    
    def _combine_explanations(self, neural_importance: Dict[str, Any], 
                            symbolic_reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """Combine neural and symbolic explanations."""
        return {
            "method": "neuro_symbolic_fusion",
            "primary_features": neural_importance["most_important"],
            "symbolic_rules": symbolic_reasoning["rules_applied"],
            "confidence": symbolic_reasoning["confidence"],
            "explanation": f"Primary features {neural_importance['most_important']} " 
                          f"triggered rules: {symbolic_reasoning['rules_applied']}"
        }
    
    def evaluate(self, X: Union[np.ndarray, pd.DataFrame], 
                y: Union[np.ndarray, pd.DataFrame]) -> Dict[str, float]:
        """Evaluate model performance.
        
        Args:
            X: Test features
            y: True labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)
        
        return {
            "accuracy": accuracy_score(y, predictions),
            "precision": precision_score(y, predictions, average='weighted'),
            "recall": recall_score(y, predictions, average='weighted'),
            "f1_score": f1_score(y, predictions, average='weighted'),
            "explainability_score": self._calculate_explainability_score(probabilities),
            "robustness_score": self._calculate_robustness_score(X, y)
        }
    
    def _calculate_explainability_score(self, probabilities: np.ndarray) -> float:
        """Calculate explainability score based on prediction confidence distribution."""
        # Higher average confidence suggests more explainable predictions
        max_probs = np.max(probabilities, axis=1)
        return np.mean(max_probs)
    
    def _calculate_robustness_score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate robustness score using adversarial perturbations."""
        # Simplified robustness test
        noise = np.random.normal(0, 0.01, X.shape)
        perturbed_X = X + noise
        
        original_preds = self.predict(X)
        perturbed_preds = self.predict(perturbed_X)
        
        # Higher consistency indicates better robustness
        consistency = np.mean(original_preds == perturbed_preds)
        return consistency


class SimpleReasoner(BaseReasoner):
    """Simple symbolic reasoning engine for demonstration."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.rules = config.get('rules', [])
        self.output_size = 32  # Default symbolic representation size
    
    def reason(self, facts: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """Perform simple rule-based reasoning."""
        results = {"facts": facts, "query": query, "rules_applied": []}
        
        # Simplified reasoning logic
        if query == "classify":
            results["features"] = torch.randn(self.output_size)
        elif query == "explain_classification":
            results["rules_applied"] = ["rule_1", "rule_2"]
            results["steps"] = ["Analyze features", "Apply rules", "Conclude"]
            results["confidence"] = 0.85
        
        return results
    
    def add_knowledge(self, knowledge: Dict[str, Any]) -> None:
        """Add knowledge to the reasoner."""
        self.rules.extend(knowledge.get('rules', []))
    
    def explain_reasoning(self, reasoning_result: Dict[str, Any]) -> str:
        """Explain the reasoning process."""
        return f"Applied {len(reasoning_result['rules_applied'])} rules with {len(reasoning_result['steps'])} steps"
    
    def get_output_size(self) -> int:
        """Get the size of symbolic representation."""
        return self.output_size


class AttentionFusion(nn.Module):
    """Attention-based fusion of neural and symbolic components."""
    
    def __init__(self, neural_size: int, symbolic_size: int, num_classes: int):
        super().__init__()
        self.neural_size = neural_size
        self.symbolic_size = symbolic_size
        
        # Attention mechanism
        self.attention = nn.MultiheadAttention(
            embed_dim=neural_size + symbolic_size,
            num_heads=8,
            batch_first=True
        )
        
        # Output layer
        self.output_layer = nn.Sequential(
            nn.Linear(neural_size + symbolic_size, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, neural_features: torch.Tensor, symbolic_features: torch.Tensor) -> torch.Tensor:
        """Forward pass through attention fusion."""
        # Combine features
        combined = torch.cat([neural_features, symbolic_features], dim=1)
        
        # Apply attention (reshaped for attention mechanism)
        combined_reshaped = combined.unsqueeze(1)
        attended, _ = self.attention(combined_reshaped, combined_reshaped, combined_reshaped)
        attended = attended.squeeze(1)
        
        # Output
        return self.output_layer(attended)
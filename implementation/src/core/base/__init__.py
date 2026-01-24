"""
Base classes and interfaces for claw-son-four-point-five implementation.

This module provides abstract base classes that define the interfaces
for all models, pipelines, and components in the system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd


class BaseModel(ABC):
    """Abstract base class for all models in the system."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize model with configuration.
        
        Args:
            config: Model configuration dictionary
        """
        self.config = config
        self.is_trained = False
        self.model_version = None
        self.metadata = {}
    
    @abstractmethod
    def fit(self, X: Union[np.ndarray, pd.DataFrame], 
            y: Union[np.ndarray, pd.DataFrame]) -> 'BaseModel':
        """Train the model on training data.
        
        Args:
            X: Training features
            y: Training targets
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def predict(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Make predictions on new data.
        
        Args:
            X: Input features
            
        Returns:
            Predictions
        """
        pass
    
    def predict_proba(self, X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
        """Predict class probabilities (for classification tasks).
        
        Args:
            X: Input features
            
        Returns:
            Class probabilities
        """
        raise NotImplementedError("Probability prediction not implemented")
    
    @abstractmethod
    def explain(self, X: Union[np.ndarray, pd.DataFrame]) -> Dict[str, Any]:
        """Provide explanation for predictions.
        
        Args:
            X: Input features to explain
            
        Returns:
            Explanation dictionary
        """
        pass
    
    @abstractmethod
    def evaluate(self, X: Union[np.ndarray, pd.DataFrame], 
                y: Union[np.ndarray, pd.DataFrame]) -> Dict[str, float]:
        """Evaluate model performance.
        
        Args:
            X: Test features
            y: True labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        pass
    
    def save_model(self, path: str) -> None:
        """Save model to disk.
        
        Args:
            path: Path to save model
        """
        raise NotImplementedError("Model saving not implemented")
    
    def load_model(self, path: str) -> None:
        """Load model from disk.
        
        Args:
            path: Path to load model from
        """
        raise NotImplementedError("Model loading not implemented")
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get model metadata.
        
        Returns:
            Dictionary containing model metadata
        """
        return {
            "config": self.config,
            "is_trained": self.is_trained,
            "version": self.model_version,
            "metadata": self.metadata
        }


class BasePipeline(ABC):
    """Abstract base class for all data processing pipelines."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize pipeline with configuration.
        
        Args:
            config: Pipeline configuration dictionary
        """
        self.config = config
        self.steps = []
        self.is_fitted = False
    
    @abstractmethod
    def fit(self, X: Union[np.ndarray, pd.DataFrame], 
            y: Optional[Union[np.ndarray, pd.DataFrame]] = None) -> 'BasePipeline':
        """Fit pipeline on training data.
        
        Args:
            X: Training features
            y: Optional training targets
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def transform(self, X: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Transform data using fitted pipeline.
        
        Args:
            X: Input data to transform
            
        Returns:
            Transformed data
        """
        pass
    
    def fit_transform(self, X: Union[np.ndarray, pd.DataFrame], 
                     y: Optional[Union[np.ndarray, pd.DataFrame]] = None) -> Union[np.ndarray, pd.DataFrame]:
        """Fit pipeline and transform data.
        
        Args:
            X: Input data
            y: Optional targets
            
        Returns:
            Transformed data
        """
        return self.fit(X, y).transform(X)
    
    @abstractmethod
    def get_params(self) -> Dict[str, Any]:
        """Get pipeline parameters.
        
        Returns:
            Dictionary of parameters
        """
        pass
    
    @abstractmethod
    def set_params(self, **params) -> 'BasePipeline':
        """Set pipeline parameters.
        
        Args:
            **params: Parameters to set
            
        Returns:
            Self for method chaining
        """
        pass


class BaseReasoner(ABC):
    """Abstract base class for reasoning systems."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize reasoner with configuration.
        
        Args:
            config: Reasoner configuration dictionary
        """
        self.config = config
        self.knowledge_base = None
    
    @abstractmethod
    def reason(self, facts: List[Dict[str, Any]], 
               query: str) -> Dict[str, Any]:
        """Perform reasoning on given facts.
        
        Args:
            facts: List of facts for reasoning
            query: Reasoning query
            
        Returns:
            Reasoning results
        """
        pass
    
    @abstractmethod
    def add_knowledge(self, knowledge: Dict[str, Any]) -> None:
        """Add knowledge to the reasoning system.
        
        Args:
            knowledge: Knowledge to add
        """
        pass
    
    @abstractmethod
    def explain_reasoning(self, reasoning_result: Dict[str, Any]) -> str:
        """Explain the reasoning process.
        
        Args:
            reasoning_result: Result to explain
            
        Returns:
            Explanation of reasoning process
        """
        pass


class BaseExplainer(ABC):
    """Abstract base class for explanation methods."""
    
    def __init__(self, model: BaseModel, config: Dict[str, Any]):
        """Initialize explainer with model and configuration.
        
        Args:
            model: Model to explain
            config: Explainer configuration
        """
        self.model = model
        self.config = config
    
    @abstractmethod
    def explain_instance(self, X: Union[np.ndarray, pd.DataFrame], 
                       X_reference: Optional[Union[np.ndarray, pd.DataFrame]] = None) -> Dict[str, Any]:
        """Explain a single prediction instance.
        
        Args:
            X: Instance to explain
            X_reference: Reference/background instances
            
        Returns:
            Explanation dictionary
        """
        pass
    
    @abstractmethod
    def explain_global(self) -> Dict[str, Any]:
        """Explain global model behavior.
        
        Returns:
            Global explanation dictionary
        """
        pass
    
    @abstractmethod
    def visualize_explanation(self, explanation: Dict[str, Any]) -> Any:
        """Create visualization of explanation.
        
        Args:
            explanation: Explanation to visualize
            
        Returns:
            Visualization object
        """
        pass


class BaseDataProcessor(ABC):
    """Abstract base class for data processing components."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize data processor with configuration.
        
        Args:
            config: Data processor configuration
        """
        self.config = config
        self.is_fitted = False
    
    @abstractmethod
    def fit(self, X: Union[np.ndarray, pd.DataFrame]) -> 'BaseDataProcessor':
        """Fit data processor on data.
        
        Args:
            X: Data to fit on
            
        Returns:
            Self for method chaining
        """
        pass
    
    @abstractmethod
    def transform(self, X: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Transform data.
        
        Args:
            X: Data to transform
            
        Returns:
            Transformed data
        """
        pass
    
    def fit_transform(self, X: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Fit and transform data.
        
        Args:
            X: Data to process
            
        Returns:
            Processed data
        """
        return self.fit(X).transform(X)
    
    @abstractmethod
    def inverse_transform(self, X: Union[np.ndarray, pd.DataFrame]) -> Union[np.ndarray, pd.DataFrame]:
        """Inverse transform data.
        
        Args:
            X: Transformed data
            
        Returns:
            Original scale data
        """
        pass


class BaseEvaluator(ABC):
    """Abstract base class for model evaluation."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize evaluator with configuration.
        
        Args:
            config: Evaluation configuration
        """
        self.config = config
        self.metrics = {}
    
    @abstractmethod
    def evaluate_classification(self, y_true: np.ndarray, y_pred: np.ndarray, 
                             y_proba: Optional[np.ndarray] = None) -> Dict[str, float]:
        """Evaluate classification model.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities
            
        Returns:
            Dictionary of classification metrics
        """
        pass
    
    @abstractmethod
    def evaluate_regression(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Evaluate regression model.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Dictionary of regression metrics
        """
        pass
    
    @abstractmethod
    def evaluate_explainability(self, model: BaseModel, 
                              X_test: Union[np.ndarray, pd.DataFrame]) -> Dict[str, float]:
        """Evaluate model explainability.
        
        Args:
            model: Model to evaluate
            X_test: Test data
            
        Returns:
            Dictionary of explainability metrics
        """
        pass
    
    @abstractmethod
    def evaluate_robustness(self, model: BaseModel, 
                           X_test: Union[np.ndarray, pd.DataFrame], 
                           y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model robustness.
        
        Args:
            model: Model to evaluate
            X_test: Test data
            y_test: True labels
            
        Returns:
            Dictionary of robustness metrics
        """
        pass


class BaseConfigValidator:
    """Base class for configuration validation."""
    
    @staticmethod
    @abstractmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration dictionary.
        
        Args:
            config: Configuration to validate
            
        Returns:
            True if valid, raises Exception if invalid
        """
        pass
    
    @staticmethod
    @abstractmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Default configuration dictionary
        """
        pass


class BaseLogger:
    """Base class for logging and monitoring."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize logger with configuration.
        
        Args:
            config: Logger configuration
        """
        self.config = config
    
    @abstractmethod
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None) -> None:
        """Log metrics.
        
        Args:
            metrics: Metrics to log
            step: Optional step number
        """
        pass
    
    @abstractmethod
    def log_artifact(self, artifact_path: str, artifact_name: str) -> None:
        """Log artifact.
        
        Args:
            artifact_path: Path to artifact
            artifact_name: Name of artifact
        """
        pass
    
    @abstractmethod
    def log_model(self, model: BaseModel, model_name: str) -> None:
        """Log model.
        
        Args:
            model: Model to log
            model_name: Name of model
        """
        pass
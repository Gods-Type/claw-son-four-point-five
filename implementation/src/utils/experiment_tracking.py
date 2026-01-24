"""
Experiment tracking framework for claw-son-four-point-five implementation.

This module provides comprehensive experiment tracking with MLflow integration,
including automated logging, parameter management, and result visualization.
"""

import os
import json
import yaml
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

import mlflow
import mlflow.pytorch
import mlflow.sklearn
import pandas as pd
import numpy as np
from mlflow.tracking import MlflowClient

logger = logging.getLogger(__name__)


class ExperimentTracker:
    """
    Comprehensive experiment tracking with MLflow integration.
    
    Provides automated logging for:
    - Model parameters and hyperparameters
    - Training and evaluation metrics
    - Model artifacts and checkpoints
    - Data versions and preprocessing steps
    - System metrics and environment details
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize experiment tracker.
        
        Args:
            config: Experiment tracking configuration containing:
                - tracking_uri: MLflow tracking server URI
                - experiment_name: Name of experiment
                - run_name: Optional run name
                - auto_logging: Enable automatic logging
                - tags: Dictionary of tags to add to runs
        """
        self.config = config
        self.tracking_uri = config.get('tracking_uri', 'http://localhost:5000')
        self.experiment_name = config.get('experiment_name', 'claw_son_experiments')
        self.run_name = config.get('run_name')
        self.auto_logging = config.get('auto_logging', True)
        self.tags = config.get('tags', {})
        
        # Initialize MLflow
        self._setup_mlflow()
        
        # Initialize experiment
        self.experiment_id = self._get_or_create_experiment()
        
        # Current run tracking
        self.current_run = None
        self.client = MlflowClient(tracking_uri=self.tracking_uri)
        
        logger.info(f"Initialized ExperimentTracker for experiment: {self.experiment_name}")
    
    def _setup_mlflow(self):
        """Setup MLflow configuration."""
        mlflow.set_tracking_uri(self.tracking_uri)
        
        # Enable auto logging for supported libraries
        if self.auto_logging:
            mlflow.pytorch.autolog()
            mlflow.sklearn.autolog()
        
        logger.info(f"MLflow tracking configured at: {self.tracking_uri}")
    
    def _get_or_create_experiment(self) -> str:
        """Get existing experiment or create new one."""
        try:
            experiment = mlflow.get_experiment_by_name(self.experiment_name)
            if experiment:
                return experiment.experiment_id
            else:
                experiment_id = mlflow.create_experiment(
                    name=self.experiment_name,
                    tags=self.tags
                )
                logger.info(f"Created new experiment: {self.experiment_name}")
                return experiment_id
        except Exception as e:
            logger.error(f"Failed to get or create experiment: {e}")
            raise
    
    def start_run(self, run_name: Optional[str] = None, 
                 tags: Optional[Dict[str, str]] = None) -> str:
        """Start a new MLflow run.
        
        Args:
            run_name: Name for the run (overrides config)
            tags: Additional tags for the run
            
        Returns:
            Run ID
        """
        run_name = run_name or self.run_name or f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Merge tags
        run_tags = {**self.tags}
        if tags:
            run_tags.update(tags)
        
        # Start run
        self.current_run = mlflow.start_run(
            experiment_id=self.experiment_id,
            run_name=run_name,
            tags=run_tags
        )
        
        logger.info(f"Started MLflow run: {self.current_run.info.run_id}")
        return self.current_run.info.run_id
    
    def end_run(self, status: str = "FINISHED") -> None:
        """End the current MLflow run.
        
        Args:
            status: Run status (FINISHED, FAILED, KILLED)
        """
        if self.current_run:
            mlflow.end_run(status=status)
            logger.info(f"Ended run with status: {status}")
            self.current_run = None
    
    def log_parameters(self, params: Dict[str, Any]) -> None:
        """Log parameters to current run.
        
        Args:
            params: Dictionary of parameters to log
        """
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        for key, value in params.items():
            mlflow.log_param(key, value)
        
        logger.info(f"Logged {len(params)} parameters")
    
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None) -> None:
        """Log metrics to current run.
        
        Args:
            metrics: Dictionary of metrics to log
            step: Optional step number for logging
        """
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        for key, value in metrics.items():
            mlflow.log_metric(key, value, step=step)
        
        logger.info(f"Logged {len(metrics)} metrics at step {step}")
    
    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None) -> None:
        """Log artifact to current run.
        
        Args:
            local_path: Path to local artifact file
            artifact_path: Destination path in MLflow
        """
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        mlflow.log_artifact(local_path, artifact_path)
        logger.info(f"Logged artifact: {local_path}")
    
    def log_model(self, model, model_name: str, framework: str = "pytorch") -> None:
        """Log model to current run.
        
        Args:
            model: Trained model object
            model_name: Name for the model
            framework: ML framework used
        """
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        if framework.lower() == "pytorch":
            mlflow.pytorch.log_model(model, model_name)
        elif framework.lower() == "sklearn":
            mlflow.sklearn.log_model(model, model_name)
        else:
            # Generic model logging
            mlflow.log_model(model, model_name)
        
        logger.info(f"Logged model: {model_name} ({framework})")
    
    def log_dataset_info(self, dataset_info: Dict[str, Any]) -> None:
        """Log dataset information.
        
        Args:
            dataset_info: Dictionary containing dataset information
        """
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        # Log as parameters
        for key, value in dataset_info.items():
            if isinstance(value, (str, int, float, bool)):
                mlflow.log_param(f"dataset_{key}", value)
            else:
                # Log complex objects as JSON artifact
                artifact_path = f"dataset_{key}.json"
                with open(artifact_path, 'w') as f:
                    json.dump(value, f, indent=2, default=str)
                mlflow.log_artifact(artifact_path)
                os.remove(artifact_path)
        
        logger.info(f"Logged dataset information: {list(dataset_info.keys())}")
    
    def log_system_info(self) -> None:
        """Log system information automatically."""
        if not self.current_run:
            raise ValueError("No active run. Call start_run() first.")
        
        import sys
        import platform
        import torch
        
        system_info = {
            "python_version": sys.version,
            "platform": platform.platform(),
            "torch_version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
        }
        
        for key, value in system_info.items():
            mlflow.log_param(f"system_{key}", str(value))
        
        logger.info("Logged system information")
    
    def get_run_history(self, run_id: Optional[str] = None) -> pd.DataFrame:
        """Get run history as DataFrame.
        
        Args:
            run_id: Run ID (if None, uses current run)
            
        Returns:
            DataFrame with run history
        """
        run_id = run_id or (self.current_run.info.run_id if self.current_run else None)
        if not run_id:
            raise ValueError("No run ID provided and no active run.")
        
        # Get run data
        run = self.client.get_run(run_id)
        metrics = run.data.metrics
        params = run.data.params
        
        # Convert to DataFrames
        metrics_df = pd.DataFrame(list(metrics.items()), columns=['metric', 'value'])
        params_df = pd.DataFrame(list(params.items()), columns=['parameter', 'value'])
        
        return {
            'metrics': metrics_df,
            'parameters': params_df,
            'run_info': run.info
        }
    
    def compare_runs(self, run_ids: List[str], 
                    metric_names: List[str]) -> pd.DataFrame:
        """Compare multiple runs.
        
        Args:
            run_ids: List of run IDs to compare
            metric_names: List of metrics to compare
            
        Returns:
            DataFrame with comparison results
        """
        comparison_data = []
        
        for run_id in run_ids:
            run = self.client.get_run(run_id)
            run_data = {'run_id': run_id, 'run_name': run.info.run_name}
            
            # Add metrics
            for metric_name in metric_names:
                metric_value = run.data.metrics.get(metric_name)
                run_data[metric_name] = metric_value
            
            comparison_data.append(run_data)
        
        return pd.DataFrame(comparison_data)
    
    def get_best_run(self, metric_name: str, 
                    direction: str = "maximize") -> Optional[str]:
        """Get best run based on metric.
        
        Args:
            metric_name: Name of metric to optimize
            direction: "maximize" or "minimize"
            
        Returns:
            Best run ID or None
        """
        # Get all runs for experiment
        runs = self.client.search_runs(
            experiment_ids=[self.experiment_id],
            order_by=[f"metrics.{metric_name} {'DESC' if direction == 'maximize' else 'ASC'}"]
        )
        
        if runs:
            return runs[0].info.run_id
        return None


class ExperimentManager:
    """High-level experiment management with configuration support."""
    
    def __init__(self, config_path: str):
        """Initialize experiment manager.
        
        Args:
            config_path: Path to experiment configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.tracker = ExperimentTracker(self.config.get('tracking', {}))
        
        logger.info(f"Initialized ExperimentManager with config: {config_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load experiment configuration."""
        if self.config_path.suffix == '.yaml':
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        elif self.config_path.suffix == '.json':
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {self.config_path.suffix}")
    
    def run_experiment(self, experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a complete experiment with tracking.
        
        Args:
            experiment_config: Configuration for the experiment
            
        Returns:
            Experiment results
        """
        # Start run
        run_id = self.tracker.start_run(
            run_name=experiment_config.get('name'),
            tags=experiment_config.get('tags')
        )
        
        try:
            # Log parameters
            self.tracker.log_parameters(experiment_config.get('parameters', {}))
            
            # Log system info
            self.tracker.log_system_info()
            
            # Log dataset info
            self.tracker.log_dataset_info(experiment_config.get('dataset', {}))
            
            # Execute experiment (placeholder for actual experiment logic)
            results = self._execute_experiment(experiment_config)
            
            # Log metrics
            self.tracker.log_metrics(results.get('metrics', {}))
            
            # Log model if trained
            if 'model' in results:
                self.tracker.log_model(
                    results['model'],
                    experiment_config.get('model_name', 'model'),
                    experiment_config.get('framework', 'pytorch')
                )
            
            # Log artifacts
            for artifact in experiment_config.get('artifacts', []):
                self.tracker.log_artifact(artifact)
            
            # End run successfully
            self.tracker.end_run("FINISHED")
            
            return {
                'run_id': run_id,
                'status': 'success',
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Experiment failed: {e}")
            self.tracker.end_run("FAILED")
            return {
                'run_id': run_id,
                'status': 'failed',
                'error': str(e)
            }
    
    def _execute_experiment(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute experiment logic (placeholder).
        
        Args:
            config: Experiment configuration
            
        Returns:
            Experiment results
        """
        # This is a placeholder for actual experiment execution
        # In real implementation, this would:
        # 1. Load data
        # 2. Initialize model
        # 3. Train model
        # 4. Evaluate model
        # 5. Return results
        
        import torch
        import torch.nn as nn
        import numpy as np
        
        # Simulate training and evaluation
        epochs = config.get('parameters', {}).get('epochs', 10)
        learning_rate = config.get('parameters', {}).get('learning_rate', 0.001)
        
        # Simulated metrics
        metrics = {
            'accuracy': np.random.uniform(0.8, 0.95),
            'loss': np.random.uniform(0.1, 0.3),
            'f1_score': np.random.uniform(0.75, 0.90),
            'precision': np.random.uniform(0.8, 0.95),
            'recall': np.random.uniform(0.75, 0.90),
            'explainability_score': np.random.uniform(0.6, 0.9),
            'robustness_score': np.random.uniform(0.7, 0.95)
        }
        
        # Create dummy model for demonstration
        dummy_model = nn.Sequential(
            nn.Linear(10, 5),
            nn.ReLU(),
            nn.Linear(5, 1)
        )
        
        return {
            'metrics': metrics,
            'model': dummy_model,
            'training_time': epochs * 0.1,  # Simulated time
            'config_used': config
        }
    
    def create_experiment_report(self, run_ids: List[str]) -> str:
        """Create comprehensive experiment report.
        
        Args:
            run_ids: List of run IDs to include in report
            
        Returns:
            Path to generated report file
        """
        # Collect all run data
        all_runs = []
        for run_id in run_ids:
            run_data = self.tracker.get_run_history(run_id)
            all_runs.append(run_data)
        
        # Generate report (simplified)
        report_path = f"experiment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        # This would generate a detailed HTML report with:
        # - Summary statistics
        # - Comparison plots
        # - Parameter analysis
        # - Performance metrics
        # - Recommendations
        
        with open(report_path, 'w') as f:
            f.write(f"""
            <html>
            <head><title>Experiment Report</title></head>
            <body>
            <h1>Experiment Report</h1>
            <p>Generated on: {datetime.now()}</p>
            <h2>Runs Analyzed: {len(run_ids)}</h2>
            <h2>Summary</h2>
            <p>Detailed report generation would go here...</p>
            </body>
            </html>
            """)
        
        logger.info(f"Generated experiment report: {report_path}")
        return report_path
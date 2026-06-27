"""
Local Interpretable Model-agnostic Explanations (LIME) Execution Pipeline.

This module provides a standalone, production-ready framework for initializing 
tabular explainers, implementing prediction wrappers, and extracting local 
feature attributions for individual instances.
"""

from typing import Callable, Union, List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from lime.lime_tabular import LimeTabularExplainer


class LimeExplanationPipeline:
    """Standalone container class for configuring and executing LIME explanations."""

    def __init__(
        self,
        X_train: pd.DataFrame,
        mode: str = "regression",
        kernel_width: Optional[float] = None,
        random_state: int = 42
    ):
        """Initializes the baseline LimeTabularExplainer container.

        Parameters:
        -----------
        X_train : pd.DataFrame
            Reference training framework dataset to extract statistics from.
        mode : str
            Operational target mode: 'regression' or 'classification'.
        kernel_width : float, optional
            Width of the exponential smoothing kernel for proximity calculations.
        random_state : int
            Deterministic seed used by the perturbation generator.
        """
        self.feature_names = X_train.columns.tolist()
        self.mode = mode
        
        # Initialize tabular explainer
        self.explainer = LimeTabularExplainer(
            training_data=X_train.values,
            feature_names=self.feature_names,
            mode=self.mode,
            kernel_width=kernel_width,
            random_state=random_state
        )

    def explain_instance(
        self,
        instance: np.ndarray,
        predict_fn: Callable[[np.ndarray], np.ndarray],
        num_features: int = 5,
        num_samples: int = 5000
    ) -> Tuple[List[Tuple[str, float]], float]:
        """Generates local feature attribution weights for a single target instance.

        Parameters:
        -----------
        instance : np.ndarray
            A 1D array representing the feature values of the instance to explain.
        predict_fn : Callable[[np.ndarray], np.ndarray]
            Prediction method wrapper that accepts a 2D numpy array and returns 
            numerical outputs.
        num_features : int
            The number of key features to retain in the sparse local explanation model.
        num_samples : int
            The size of the synthetic perturbation dataset generated around the instance.

        Returns:
        --------
        local_attributions : List[Tuple[str, float]]
            A list of tuples pairing feature text descriptors with their linear weights.
        local_r2 : float
            The R-squared score indicating how faithfully the linear surrogate 
            approximates the black box within the local neighborhood.
        """
        # Execute local explanation routines
        exp = self.explainer.explain_instance(
            data_row=instance,
            predict_fn=predict_fn,
            num_features=num_features,
            num_samples=num_samples
        )
        
        local_attributions = exp.as_list()
        local_r2 = float(exp.score)
        
        return local_attributions, local_r2


if __name__ == "__main__":
    # Standalone pipeline verification using synthetic arrays
    from sklearn.ensemble import RandomForestRegressor
    
    print("Constructing synthetic environment structures...")
    np.random.seed(42)
    labels = [f"Feature_{i}" for i in range(5)]
    
    # Generate mock training dataset
    X_mock_train = pd.DataFrame(np.random.randn(200, 5), columns=labels)
    y_mock_train = X_mock_train["Feature_0"] * 2.0 - X_mock_train["Feature_1"] * 1.5
    
    # Train a baseline black-box regressor model
    black_box_model = RandomForestRegressor(n_estimators=50, random_state=42)
    black_box_model.fit(X_mock_train, y_mock_train)
    
    # Isolate a query instance to explain
    query_instance = np.array([1.2, -0.8, 0.1, 0.5, -0.2])
    
    # Define an interface wrapper function to standardize prediction signatures
    def model_prediction_wrapper(raw_input_matrix: np.ndarray) -> np.ndarray:
        """Standardizes input formatting for black-box models during perturbation checks."""
        # Ensure data format matches the structure expected by the underlying model
        return black_box_model.predict(raw_input_matrix)

    # Initialize and run the explanation pipeline
    pipeline = LimeExplanationPipeline(X_train=X_mock_train, mode="regression")
    
    attributions, score = pipeline.explain_instance(
        instance=query_instance,
        predict_fn=model_prediction_wrapper,
        num_features=3
    )
    
    print(f"\nLocal Explanation Extraction Complete (Surrogate R2 Local Score: {score:.4f}):")
    for condition, attribution_weight in attributions:
        print(f"  -> Local Condition: {condition:25} | Attribution Weight: {attribution_weight:+.4f}")
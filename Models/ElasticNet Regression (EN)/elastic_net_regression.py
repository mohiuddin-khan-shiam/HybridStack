"""
ElasticNet Regression Pipeline with Grid Search Cross-Validation.

This module provides a standalone, production-ready pipeline configuration 
for executing hyperparameter grid optimization and fitting an ElasticNet 
Regression model independent of specific project details.
"""

import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV


def execute_elastic_net_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and runs a GridSearchCV pipeline for ElasticNet Regression.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target continuous vector.
    param_grid : dict, optional
        Dictionary specifying alpha and l1_ratio hyperparameter search choices.
    cv : int
        Number of cross-validation splitting folds.
    scoring : str
        Evaluation metric used to score and rank hyperparameter configurations.
    n_jobs : int
        Number of parallel worker processes. -1 assigns all available cores.

    Returns:
    --------
    grid_search : GridSearchCV
        The fitted grid search pipeline object containing optimization results.
    """
    # Initialize the base ElasticNet linear model estimator
    elastic_net_model = ElasticNet()

    # Define standard cross-validation search bounds if not customized
    if param_grid is None:
        param_grid = {
            "alpha": [0.001, 0.01, 0.1, 1.0, 10.0],
            "l1_ratio": [0.1, 0.3, 0.5, 0.7, 0.9],
        }

    # Construct cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=elastic_net_model,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        verbose=1,
        n_jobs=n_jobs,
    )

    # Perform structural optimization fit routines
    grid_search.fit(X_train, y_train)

    return grid_search


if __name__ == "__main__":
    # Setup random seeds for reproducible synthetic tests
    np.random.seed(42)

    print("Constructing synthetic dataset matrix blocks...")
    X_tr = np.random.randn(150, 8)
    y_tr = np.random.randn(150)
    X_te = np.random.randn(25, 8)

    print("Executing hyperparameter grid search optimization...")
    search_pipeline = execute_elastic_net_grid_search(X_train=X_tr, y_train=y_tr)

    print("\nOptimal Parameters Selected:")
    for key, val in search_pipeline.best_params_.items():
        print(f"  {key}: {val}")

    # Extract optimal model instance
    best_model = search_pipeline.best_estimator_

    # Run inference test
    predictions = best_model.predict(X_te)
    print(f"\nInference execution complete. Predictions array shape: {predictions.shape}")
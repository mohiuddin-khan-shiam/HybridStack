"""
K-Nearest Neighbors (KNN) Regressor Pipeline.

This module provides a standalone, production-ready pipeline configuration 
for executing Grid Search Cross-Validation and final model optimization using 
Scikit-Learn's KNeighborsRegressor framework.
"""

import warnings
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsRegressor

# Suppress potential internal runtime casting warnings raised by Scikit-Learn structures
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message="invalid value encountered in cast",
)


def execute_knn_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and runs a GridSearchCV pipeline for a K-Nearest Neighbors Regressor.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target continuous vector.
    param_grid : dict, optional
        Dictionary specifying the hyperparameter search space configurations.
    cv : int
        Number of cross-validation splitting folds.
    scoring : str
        Evaluation metric used to rank hyperparameter configurations.
    n_jobs : int
        Number of parallel worker processes. -1 assigns all available cores.

    Returns:
    --------
    grid_search : GridSearchCV
        The fitted grid search pipeline object containing optimization results.
    """
    # Initialize the base K-Nearest Neighbors estimator
    knn_model = KNeighborsRegressor()

    # Establish default parameter space dimensions if not customized
    if param_grid is None:
        param_grid = {
            "n_neighbors": [3, 5, 7, 10, 15],
            "weights": ["uniform", "distance"],
            "p": [1, 2],  # p=1 maps to Manhattan, p=2 maps to Euclidean
        }

    # Construct the cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=knn_model,
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
    X_tr = np.random.randn(150, 4)
    y_tr = np.random.randn(150)
    X_te = np.random.randn(20, 4)

    print("Executing hyperparameter grid search optimization...")
    search_pipeline = execute_knn_grid_search(X_train=X_tr, y_train=y_tr)

    print("\nOptimal Parameters Selected:")
    for key, val in search_pipeline.best_params_.items():
        print(f"  {key}: {val}")

    # Extract optimal model instance
    best_model = search_pipeline.best_estimator_

    # Run inference test
    predictions = best_model.predict(X_te)
    print(f"\nInference execution complete. Predictions array shape: {predictions.shape}")
"""
Extremely Randomized Trees (Extra Trees) Regressor Pipeline.

This module provides a standalone, production-ready pipeline configuration 
for executing Grid Search Cross-Validation and final model optimization using 
the ExtraTreesRegressor framework.
"""

import warnings
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import GridSearchCV

# Suppress potential internal casting warnings raised by Scikit-Learn structures
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message="invalid value encountered in cast",
)


def execute_extra_trees_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    random_state: int = 42,
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and runs a GridSearchCV pipeline for an Extra Trees Regressor.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target continuous vector.
    param_grid : dict, optional
        Dictionary specifying hyperparameter search options.
    cv : int
        Number of cross-validation splitting folds.
    scoring : str
        Evaluation metric used to rank hyperparameter configurations.
    random_state : int
        Seed used by the internal random number generator for reproducibility.
    n_jobs : int
        Number of parallel worker processes. -1 assigns all available cores.

    Returns:
    --------
    grid_search : GridSearchCV
        The fitted grid search pipeline object containing optimization results.
    """
    # Initialize the base extremely randomized trees estimator
    et_model = ExtraTreesRegressor(random_state=random_state)

    # Establish default parameter space dimensions if not customized
    if param_grid is None:
        param_grid = {
            "n_estimators": [100, 200, 500],
            "max_depth": [3, 5, 10],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 5, 10],
            "bootstrap": [True, False],
        }

    # Construct the cross-validation grid search wrapper
    grid_search = GridSearchCV(
        estimator=et_model,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        verbose=1,
        n_jobs=n_jobs,
    )

    # Perform optimization fit routines
    grid_search.fit(X_train, y_train)

    return grid_search


if __name__ == "__main__":
    # Setup random seeds for reproducible synthetic tests
    np.random.seed(42)

    print("Constructing synthetic dataset matrix blocks...")
    X_tr = np.random.randn(120, 8)
    y_tr = np.random.randn(120)
    X_te = np.random.randn(30, 8)

    print("Executing hyperparameter grid search optimization...")
    search_pipeline = execute_extra_trees_grid_search(X_train=X_tr, y_train=y_tr)

    print("\nOptimal Parameters Selected:")
    for key, val in search_pipeline.best_params_.items():
        print(f"  {key}: {val}")

    # Extract optimal model instance
    best_model = search_pipeline.best_estimator_

    # Run inference test
    predictions = best_model.predict(X_te)
    print(f"\nInference execution complete. Predictions array shape: {predictions.shape}")
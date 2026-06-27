"""
Gradient Boosting Regressor Pipeline with Grid Search Cross-Validation.

This module provides a standalone, production-ready pipeline configuration 
for initializing, tuning, and optimizing a Gradient Boosting Regressor 
independent of specific project details.
"""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV


def execute_gradient_boosting_grid_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    param_grid: dict = None,
    cv: int = 5,
    scoring: str = "neg_mean_squared_error",
    random_state: int = 42,
    n_jobs: int = -1,
) -> GridSearchCV:
    """Initializes and executes a GridSearchCV pipeline for a Gradient Boosting Regressor.

    Parameters:
    -----------
    X_train : np.ndarray
        Training feature matrix.
    y_train : np.ndarray
        Training target vector.
    param_grid : dict, optional
        Dictionary containing hyperparameter choices to evaluate.
    cv : int
        Number of folds for K-fold cross-validation.
    scoring : str
        Evaluation metric used to score hyperparameter configurations.
    random_state : int
        Seed value for the internal random number generator for reproducibility.
    n_jobs : int
        Number of parallel jobs to run. -1 maps to all available CPU cores.

    Returns:
    --------
    grid_search : GridSearchCV
        The fitted grid search pipeline object containing optimization results.
    """
    # Initialize the base Gradient Boosting Regressor
    gbm_model = GradientBoostingRegressor(random_state=random_state)

    # Define default parameter grid if none is specified
    if param_grid is None:
        param_grid = {
            "n_estimators": [100, 300],
            "learning_rate": [0.05, 0.1],
            "max_depth": [3, 6],
            "min_samples_split": [10, 20],
            "subsample": [0.8, 0.9],
        }

    # Set up the Cross-Validation pipeline grid handler
    grid_search = GridSearchCV(
        estimator=gbm_model,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        verbose=1,
        n_jobs=n_jobs,
    )

    # Execute hyperparameter tuning
    grid_search.fit(X_train, y_train)

    return grid_search


if __name__ == "__main__":
    # Demonstration pipeline execution using synthetic data arrays
    print("Generating synthetic validation dataset blocks...")
    np.random.seed(42)
    X_tr = np.random.rand(100, 8)
    y_tr = np.random.rand(100)
    X_te = np.random.rand(20, 8)

    print("Running hyperparameter tuning grid search...")
    search_pipeline = execute_gradient_boosting_grid_search(X_tr, y_tr)

    print("
Optimal Hyperparameter Combination Found:")
    print(search_pipeline.best_params_)

    # Extract the top performing configured estimator model
    best_gbm_model = search_pipeline.best_estimator_

    # Execute model inference
    predictions = best_gbm_model.predict(X_te)
    print(f"
Inference execution complete. Predictions array shape: {predictions.shape}")

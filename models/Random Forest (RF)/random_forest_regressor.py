"""
Random Forest Regressor Pipeline with Randomized Search Cross-Validation.

This module provides a standalone, production-ready pipeline for initializing, 
tuning, and optimizing a Random Forest Regressor independent of specific datasets.
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV


def create_rf_search_pipeline(
    random_state: int = 42, n_iter: int = 10, cv: int = 5, n_jobs: int = -1
) -> RandomizedSearchCV:
    """Initializes and returns a RandomizedSearchCV object for a Random Forest Regressor.

    Parameters:
    -----------
    random_state : int
        Seed used by the random number generator for reproducibility.
    n_iter : int
        Number of parameter settings that are sampled. Trades off runtime vs quality.
    cv : int
        Number of folds for K-fold cross-validation.
    n_jobs : int
        The number of jobs to run in parallel. -1 means using all processors.

    Returns:
    --------
    random_search : RandomizedSearchCV
        The un-fitted search pipeline object configured with the hyperparameter grid.
    """
    # Initialize the base Random Forest Regressor
    rf_model = RandomForestRegressor(random_state=random_state)

    # Define the comprehensive parameter distribution space
    param_dist = {
        "n_estimators": [50, 100, 200],
        "max_depth": [5, 10, 15, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
    }

    # Construct the randomized search optimization pipeline
    random_search = RandomizedSearchCV(
        estimator=rf_model,
        param_distributions=param_dist,
        n_iter=n_iter,
        cv=cv,
        n_jobs=n_jobs,
        verbose=2,
        random_state=random_state,
    )

    return random_search


if __name__ == "__main__":
    # Demonstration execution with synthetic data
    print("Generating synthetic data for pipeline validation...")
    X_train = np.random.rand(100, 10)
    y_train = np.random.rand(100)
    X_test = np.random.rand(20, 10)

    # Initialize pipeline
    pipeline = create_rf_search_pipeline()

    # Fit pipeline
    print("Executing hyperparameter search...")
    pipeline.fit(X_train, y_train)

    # Retrieve optimal parameters and top-performing estimator
    print("\nBest Hyperparameters Found:")
    print(pipeline.best_params_)

    best_model = pipeline.best_estimator_

    # Generate inference predictions
    predictions = best_model.predict(X_test)
    print(f"Predictions successfully generated. Shape: {predictions.shape}")
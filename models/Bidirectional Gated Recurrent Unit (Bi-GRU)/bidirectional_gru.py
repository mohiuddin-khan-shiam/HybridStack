"""
Bidirectional Gated Recurrent Unit (BiGRU) Optimization Pipeline.

This module provides a standalone, production-ready framework for constructing,
tuning, and training a stacked Bidirectional GRU model with Optuna 
hyperparameter optimization.
"""

import os
import random
import numpy as np
import optuna
from optuna.integration import TFKerasPruningCallback
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import GRU, Dense, Dropout, Input, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam, RMSprop


def set_reproducibility(seed: int = 42):
    """Enforces strict deterministic behavior across execution environments."""
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ["TF_DETERMINISTIC_OPS"] = "1"
    tf.config.threading.set_intra_op_parallelism_threads(1)
    tf.config.threading.set_inter_op_parallelism_threads(1)
    optuna.logging.set_verbosity(optuna.logging.ERROR)


def reshape_for_rnn(X: np.ndarray) -> np.ndarray:
    """Transforms a 2D feature matrix into a 3D sequential tensor.

    Parameters:
    -----------
    X : np.ndarray
        Array of shape (samples, features).

    Returns:
    --------
    np.ndarray
        3D tensor shaped as (samples, timesteps=1, features).
    """
    return np.expand_dims(X, axis=1)


def create_bidirectional_gru_model(trial, input_shape: tuple) -> Sequential:
    """Constructs and compiles a stacked BiGRU model using Optuna suggestions.

    Parameters:
    -----------
    trial : optuna.trial.Trial
        Active trial object instance suggesting hyperparameter values.
    input_shape : tuple
        The expected input dimensions structured as (timesteps, features).

    Returns:
    --------
    model : Sequential
        A compiled Keras sequential model framework.
    """
    units = trial.suggest_categorical("units", [100, 150])
    learning_rate = trial.suggest_categorical("learning_rate", [0.001, 0.005])
    dropout_rate = trial.suggest_categorical("dropout_rate", [0.2, 0.3])
    clipnorm_value = trial.suggest_categorical("clipnorm", [2.0, 3.0])
    optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "RMSprop"])
    activation_function = trial.suggest_categorical("activation_function", ["tanh", "relu"])

    if optimizer_name == "Adam":
        optimizer = Adam(learning_rate=learning_rate, clipnorm=clipnorm_value)
    else:
        optimizer = RMSprop(learning_rate=learning_rate, clipnorm=clipnorm_value)

    model = Sequential([
        Input(shape=input_shape),
        Bidirectional(GRU(units, activation=activation_function, return_sequences=True)),
        Dropout(dropout_rate),
        Bidirectional(GRU(units, activation=activation_function)),
        Dropout(dropout_rate),
        Dense(1),
    ])

    model.compile(optimizer=optimizer, loss="mse")
    return model


class OptimizationObjective:
    """Callable objective container class for Optuna study worker execution."""

    def __init__(self, X_train: np.ndarray, y_train: np.ndarray, val_split_ratio: float = 0.8):
        self.X_train = X_train
        self.y_train = y_train
        
        split_idx = int(len(X_train) * val_split_ratio)
        self.X_tr_fold = X_train[:split_idx]
        self.y_tr_fold = y_train[:split_idx]
        self.X_val_fold = X_train[split_idx:]
        self.y_val_fold = y_train[split_idx:]
        
        self.input_shape = (X_train.shape[1], X_train.shape[2])

    def __call__(self, trial) -> float:
        model = create_bidirectional_gru_model(trial, self.input_shape)
        
        early_stopping = EarlyStopping(
            monitor="val_loss", patience=5, restore_best_weights=True, verbose=0
        )
        pruning_callback = TFKerasPruningCallback(trial, monitor="val_loss")

        batch_size = trial.suggest_categorical("batch_size", [32, 64])
        epochs = trial.suggest_categorical("epochs", [50, 100, 150])

        model.fit(
            self.X_tr_fold,
            self.y_tr_fold,
            validation_data=(self.X_val_fold, self.y_val_fold),
            batch_size=batch_size,
            epochs=epochs,
            callbacks=[early_stopping, pruning_callback],
            verbose=0,
        )

        return float(model.evaluate(self.X_val_fold, self.y_val_fold, verbose=0))


def run_pipeline(X_train_raw: np.ndarray, y_train_raw: np.ndarray, X_test_raw: np.ndarray, n_trials: int = 5):
    """Executes the complete hyperparameter search optimization and final fit pipeline."""
    set_reproducibility()

    # Preprocess arrays into sequential 3D structure dimensions
    X_train_3d = reshape_for_rnn(X_train_raw)
    X_test_3d = reshape_for_rnn(X_test_raw)

    # Initialize optimization search space study instance
    objective_callable = OptimizationObjective(X_train_3d, y_train_raw)
    study = optuna.create_study(
        direction="minimize",
        study_name="BiGRU_Optimization",
        sampler=optuna.samplers.TPESampler(seed=42),
    )
    
    print(f"Beginning hyperparameter optimization across {n_trials} trials...")
    study.optimize(objective_callable, n_trials=n_trials)
    print("Optimization complete.")
    print(f"Best Trials Validation Loss Target: {study.best_value:.5f}")

    # Fit final model container utilizing optimal parameters
    print("\nFitting final model instance with optimal hyperparameters...")
    best_model = create_bidirectional_gru_model(
        study.best_trial, input_shape=(X_train_3d.shape[1], X_train_3d.shape[2])
    )
    
    best_model.fit(
        X_train_3d,
        y_train_raw,
        batch_size=study.best_trial.params["batch_size"],
        epochs=study.best_trial.params["epochs"],
        validation_split=0.2,
        verbose=0,
    )

    predictions = best_model.predict(X_test_3d)
    return best_model, study.best_params, predictions


if __name__ == "__main__":
    # Generate dummy data vectors for standalone pipeline verification
    np.random.seed(42)
    dummy_X_train = np.random.randn(100, 10)
    dummy_y_train = np.random.randn(100)
    dummy_X_test = np.random.randn(20, 10)

    # Execute operational validation runtime
    final_model, optimal_params, test_predictions = run_pipeline(
        dummy_X_train, dummy_y_train, dummy_X_test, n_trials=2
    )
    
    print("\nOptimal Parameter Selection:")
    for k, v in optimal_params.items():
        print(f"  {k}: {v}")
    print(f"\nInference execution complete. Predictions matrix shape: {test_predictions.shape}")
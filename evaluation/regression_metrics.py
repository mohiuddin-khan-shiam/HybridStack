"""
Regression Evaluation Metrics Module

This module provides a comprehensive, production-grade suite of evaluation metrics
for continuous regression, forecasting, and statistical modeling tasks. It implements
standard error metrics, percentage-based errors, scaled errors, and goodness-of-fit
indicators using robust numerical operations, explicit input validation, and clear type hints.

Supported Metrics:
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)
- Mean Absolute Percentage Error (MAPE)
- Symmetric Mean Absolute Percentage Error (sMAPE)
- Mean Absolute Scaled Error (MASE)
- Coefficient of Determination (R²)

Design Principles:
- Independence: General-purpose, modular implementations with no project-specific dependencies.
- Reliability: Thorough error handling for mismatched lengths, empty sequences, and division-by-zero.
- Efficiency: Vectorized NumPy implementations with fallback support for standard Python sequences.
- Consistency: Standardized docstring formats (Args, Returns, Raises) to align with downstream metric modules.
"""

from typing import Union, List, Optional
import numpy as np

# Type alias for array-like inputs
ArrayLike = Union[List[float], List[int], np.ndarray]


def _validate_and_convert(y_true: ArrayLike, y_pred: ArrayLike) -> tuple[np.ndarray, np.ndarray]:
    """
    Validates input dimensions, compatibility, and types, converting inputs to 1D NumPy arrays.

    Args:
        y_true (ArrayLike): Ground truth (correct) target values.
        y_pred (ArrayLike): Estimated target values.

    Returns:
        tuple[np.ndarray, np.ndarray]: Flattened 1D NumPy arrays of (y_true, y_pred).

    Raises:
        ValueError: If inputs are empty, contain non-numeric data, have mismatched shapes,
                    or contain infinite/NaN values.
    """
    try:
        true_arr = np.asarray(y_true, dtype=np.float64).ravel()
        pred_arr = np.asarray(y_pred, dtype=np.float64).ravel()
    except (ValueError, TypeError) as e:
        raise ValueError("Inputs must be numeric arrays or lists that can be converted to float64.") from e

    if true_arr.size == 0 or pred_arr.size == 0:
        raise ValueError("Input arrays must not be empty.")

    if true_arr.shape != pred_arr.shape:
        raise ValueError(f"Shape mismatch: y_true shape {true_arr.shape} does not match y_pred shape {pred_arr.shape}.")

    if not (np.isfinite(true_arr).all() and np.isfinite(pred_arr).all()):
        raise ValueError("Input arrays contain NaNs or infinite values which are invalid for metric computation.")

    return true_arr, pred_arr


def mean_squared_error(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """
    Computes the Mean Squared Error (MSE).

    MSE measures the average of the squares of the errors—that is, the average
    squared difference between the estimated values and the actual value. It penalizes
    larger errors heavily due to the squaring operation.

    Formula:
        MSE = (1 / n) * sum((y_true - y_pred) ** 2)

    Args:
        y_true (ArrayLike): Ground truth target values.
        y_pred (ArrayLike): Predicted target values.

    Returns:
        float: Calculated MSE value.
    """
    true_arr, pred_arr = _validate_and_convert(y_true, y_pred)
    mse = np.mean((true_arr - pred_arr) ** 2)
    return float(mse)


def root_mean_squared_error(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """
    Computes the Root Mean Squared Error (RMSE).

    RMSE is the square root of the mean squared error. It brings the error metric
    back to the original scale of the target variable, making it more interpretable
    while retaining a high sensitivity to outliers.

    Formula:
        RMSE = sqrt((1 / n) * sum((y_true - y_pred) ** 2))

    Args:
        y_true (ArrayLike): Ground truth target values.
        y_pred (ArrayLike): Predicted target values.

    Returns:
        float: Calculated RMSE value.
    """
    mse = mean_squared_error(y_true, y_pred)
    return float(np.sqrt(mse))


def mean_absolute_error(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """
    Computes the Mean Absolute Error (MAE).

    MAE measures the average magnitude of the errors in a set of predictions,
    without considering their direction. It is a linear score, meaning all individual
    differences are weighted equally in the average, rendering it robust to outliers.

    Formula:
        MAE = (1 / n) * sum(|y_true - y_pred|)

    Args:
        y_true (ArrayLike): Ground truth target values.
        y_pred (ArrayLike): Predicted target values.

    Returns:
        float: Calculated MAE value.
    """
    true_arr, pred_arr = _validate_and_convert(y_true, y_pred)
    mae = np.mean(np.abs(true_arr - pred_arr))
    return float(mae)


def mean_absolute_percentage_error(y_true: ArrayLike, y_pred: ArrayLike, epsilon: float = 1e-8) -> float:
    """
    Computes the Mean Absolute Percentage Error (MAPE).

    MAPE measures the prediction accuracy of a forecasting or regression method as a percentage.
    To avoid division-by-zero errors when an element of y_true is zero, a small stability
    factor (epsilon) can be provided, or strict zero-handling can be enforced.

    Formula:
        MAPE = (100 / n) * sum(|(y_true - y_pred) / y_true|)

    Args:
        y_true (ArrayLike): Ground truth target values.
        y_pred (ArrayLike): Predicted target values.
        epsilon (float): Small positive constant added to the denominator to prevent division by zero
                         if y_true contains zeros. Default is 1e-8. If exactly 0.0 is passed, rows
                         where y_true is 0.0 will raise a ValueError.

    Returns:
        float: Calculated MAPE value as a percentage (e.g., 12.5 means 12.5%).

    Raises:
        ValueError: If epsilon is 0.0 and any element of y_true is 0.0.
    """
    true_arr, pred_arr = _validate_and_convert(y_true, y_pred)
    
    if epsilon == 0.0:
        if np.any(true_arr == 0.0):
            raise ValueError("Zero value encountered in y_true while computing MAPE with epsilon=0.0.")
        denominator = true_arr
    else:
        # Avoid zero values using signed epsilon or replacing zero directly
        denominator = np.where(true_arr == 0.0, epsilon, true_arr)

    mape = np.mean(np.abs((true_arr - pred_arr) / denominator)) * 100.0
    return float(mape)


def symmetric_mean_absolute_percentage_error(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """
    Computes the Symmetric Mean Absolute Percentage Error (sMAPE).

    sMAPE is an accuracy measure based on percentage (or relative) errors. Unlike standard MAPE,
    it limits the maximum error bound to 200% by centering the denominator around the average
    of the true and predicted absolute values, mitigating asymmetry issues.

    Formula:
        sMAPE = (200 / n) * sum(|y_true - y_pred| / (|y_true| + |y_pred|))

    Args:
        y_true (ArrayLike): Ground truth target values.
        y_pred (ArrayLike): Predicted target values.

    Returns:
        float: Calculated sMAPE value as a percentage (range: [0.0, 200.0]).
        
    Note:
        If both y_true and y_pred are 0.0 for a given point, the error for that point is defined as 0.0.
    """
    true_arr, pred_arr = _validate_and_convert(y_true, y_pred)
    
    numerator = np.abs(true_arr - pred_arr)
    denominator = np.abs(true_arr) + np.abs(pred_arr)
    
    # Handle edge case where both true and pred are 0.0
    with np.errstate(divide='ignore', invalid='ignore'):
        percentage_errors = np.where(denominator == 0.0, 0.0, numerator / denominator)
        
    smape = np.mean(percentage_errors) * 200.0
    return float(smape)


def mean_absolute_scaled_error(y_true: ArrayLike, y_pred: ArrayLike, y_train: Optional[ArrayLike] = None, periodicity: int = 1) -> float:
    """
    Computes the Mean Absolute Scaled Error (MASE).

    MASE compares the absolute errors of the model's predictions to the absolute errors
    of an in-sample naive baseline forecast. It is scale-independent, symmetric, and ideal
    for time-series analysis and forecasting evaluation.

    If `y_train` is provided, the baseline scale is computed using the in-sample training data
    (standard practice for time-series validation). If `y_train` is None, the baseline scale is
    computed out-of-sample directly from `y_true`.

    Formula:
        MAE = mean(|y_true - y_pred|)
        Scale (Non-seasonal) = mean(|y_train[i] - y_train[i - 1]|) for i = 1 to N-1
        MASE = MAE / Scale

    Args:
        y_true (ArrayLike): Ground truth target values for evaluation period.
        y_pred (ArrayLike): Predicted target values.
        y_train (Optional[ArrayLike]): Training target values used to compute the historical naive scale.
                                       If None, y_true is used to derive the baseline scale.
        periodicity (int): Seasonality parameter. Use 1 for non-seasonal data, 4 for quarterly,
                           12 for monthly data, etc. Default is 1.

    Returns:
        float: Calculated MASE value. A value < 1.0 indicates predictions are better than the naive baseline.

    Raises:
        ValueError: If the scale data contains insufficient observations for the given periodicity,
                    or if the naive baseline has zero variance (perfectly constant scale data).
    """
    true_arr, pred_arr = _validate_and_convert(y_true, y_pred)
    mae_model = np.mean(np.abs(true_arr - pred_arr))

    # Select target for computing historical baseline scale
    scale_source = np.asarray(y_train, dtype=np.float64).ravel() if y_train is not None else true_arr
    
    if scale_source.size <= periodicity:
        raise ValueError(f"Insufficient historical data points ({scale_source.size}) "
                         f"to calculate baseline scale with periodicity {periodicity}.")

    # Compute mean absolute error of the naive baseline
    naive_diff = np.abs(scale_source[periodicity:] - scale_source[:-periodicity])
    scale = np.mean(naive_diff)

    if scale == 0.0:
        raise ValueError("The naive baseline error scale is zero because the reference data is perfectly constant. "
                         "MASE cannot be computed due to division-by-zero.")

    mase = mae_model / scale
    return float(mase)


def coefficient_of_determination(y_true: ArrayLike, y_pred: ArrayLike) -> float:
    """
    Computes the Coefficient of Determination (R² Score).

    R² represents the proportion of variance in the dependent variable that is
    predictable from the independent variables. It measures the quality of fit by
    comparing the residual sum of squares against the total sum of squares of a baseline
    model predicting the mean of the ground truth.

    Formula:
        Residual Sum of Squares (SS_res) = sum((y_true - y_pred) ** 2)
        Total Sum of Squares (SS_tot) = sum((y_true - mean(y_true)) ** 2)
        R² = 1 - (SS_res / SS_tot)

    Args:
        y_true (ArrayLike): Ground truth target values.
        y_pred (ArrayLike): Predicted target values.

    Returns:
        float: Calculated R² score value. Range is (-inf, 1.0].

    Raises:
        ValueError: If all elements in y_true are identical, resulting in a total sum of squares equal to zero.
    """
    true_arr, pred_arr = _validate_and_convert(y_true, y_pred)
    
    ss_res = np.sum((true_arr - pred_arr) ** 2)
    mean_true = np.mean(true_arr)
    ss_tot = np.sum((true_arr - mean_true) ** 2)

    if ss_tot == 0.0:
        raise ValueError("The variance of y_true is zero (all actual values are identical). "
                         "R² score is undefined because the total sum of squares is zero.")

    r2 = 1.0 - (ss_res / ss_tot)
    return float(r2)


def main():
    """
    Demonstrates the practical usage of each regression metric with illustrative datasets,
    handling edge cases and validating expected outputs.
    """
    print("=" * 70)
    print(" REGRESSION EVALUATION METRICS DEMONSTRATION ")
    print("=" * 70)

    # Standard Dataset Example
    y_true = [10.0, 12.5, 14.0, 15.2, 18.0, 22.1, 19.5, 24.0, 26.3, 30.0]
    y_pred = [10.2, 11.9, 14.8, 15.0, 20.2, 21.0, 18.1, 25.5, 25.0, 31.2]
    
    # In-sample history for time series metric (MASE)
    y_train = [9.0, 9.5, 10.2, 11.0, 11.8, 12.0, 11.5, 12.2]

    print(f"Sample Size: {len(y_true)}")
    print(f"Actual Values (y_true): {y_true}")
    print(f"Predicted Values (y_pred): {y_pred}\n")

    # Computing metrics
    mse_val = mean_squared_error(y_true, y_pred)
    rmse_val = root_mean_squared_error(y_true, y_pred)
    mae_val = mean_absolute_error(y_true, y_pred)
    mape_val = mean_absolute_percentage_error(y_true, y_pred)
    smape_val = symmetric_mean_absolute_percentage_error(y_true, y_pred)
    mase_val_oos = mean_absolute_scaled_error(y_true, y_pred) # out-of-sample reference
    mase_val_is = mean_absolute_scaled_error(y_true, y_pred, y_train=y_train) # historical reference
    r2_val = coefficient_of_determination(y_true, y_pred)

    print("--- Calculated Metrics ---")
    print(f"Mean Squared Error (MSE)                     : {mse_val:.4f}")
    print(f"Root Mean Squared Error (RMSE)               : {rmse_val:.4f}")
    print(f"Mean Absolute Error (MAE)                    : {mae_val:.4f}")
    print(f"Mean Absolute Percentage Error (MAPE)        : {mape_val:.4f}%")
    print(f"Symmetric Mean Absolute Percentage Error (sMAPE): {smape_val:.4f}%")
    print(f"Mean Absolute Scaled Error (MASE, OOS Scale) : {mase_val_oos:.4f}")
    print(f"Mean Absolute Scaled Error (MASE, Train Scale): {mase_val_is:.4f}")
    print(f"Coefficient of Determination (R²)            : {r2_val:.4f}\n")

    print("--- Robustness & Robust Error Handling Tests ---")
    
    # Test 1: Shape Mismatch
    try:
        mean_squared_error([1, 2, 3], [1, 2])
    except ValueError as e:
        print(f"Caught expected error (Shape Mismatch): {e}")

    # Test 2: Target Zero Variance for R2
    try:
        coefficient_of_determination([5.0, 5.0, 5.0], [5.1, 4.9, 5.0])
    except ValueError as e:
        print(f"Caught expected error (Zero Variance R²): {e}")

    # Test 3: Zero Value in MAPE (Strict Zero Enforcement)
    try:
        mean_absolute_percentage_error([0.0, 10.0], [1.0, 9.5], epsilon=0.0)
    except ValueError as e:
        print(f"Caught expected error (Strict Zero MAPE): {e}")

    print("=" * 70)


if __name__ == "__main__":
    main()

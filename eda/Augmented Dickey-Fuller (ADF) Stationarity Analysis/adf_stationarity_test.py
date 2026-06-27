"""
Augmented Dickey-Fuller (ADF) Stationarity Analysis Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on time series data to test for stationarity. It handles data cleaning,
configures unit root regression variants (constants, trends), automates lag length selection 
via information criteria, parses test metrics, and outputs clean visualizations to assist 
with feature engineering and pipeline preparation independent of specific datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller


def run_adf_stationarity_test(
    series: pd.Series,
    regression_type: str = "c",
    autolag_criterion: str = "AIC"
) -> dict:
    """
    Executes the Augmented Dickey-Fuller formal unit root hypothesis test.
    
    Parameters:
    -----------
    series : pd.Series
        The input chronological numerical time series to evaluate.
    regression_type : str, default='c'
        The structural OLS model specification to fit:
        'c'  -> Intercept constant only (drift)
        'ct' -> Intercept constant plus a deterministic linear trend
        'nc' -> No intercept and no trend component
    autolag_criterion : str, default='AIC'
        The information criterion used to automatically select optimal lag lengths 
        ('AIC', 'BIC', or None for a fixed lag horizon).
        
    Returns:
    --------
    dict
        A dictionary containing parsed statistical metrics, critical value boundaries, 
        and an actionable interpretation statement.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("The input 'series' parameter must be a valid pandas Series object.")
        
    # Clean out missing records from the series pipeline
    clean_series = series.dropna()
    
    if len(clean_series) < 10:
        raise ValueError(f"Insufficient data volume ({len(clean_series)} points). A larger sample size is required.")
        
    # Run the underlying statistical solver
    test_output = adfuller(
        clean_series.values,
        regression=regression_type,
        autolag=autolag_criterion
    )
    
    test_statistic = test_output[0]
    p_value = test_output[1]
    lags_used = test_output[2]
    n_obs = test_output[3]
    critical_values = test_output[4]
    
    # Evaluate hypothesis boundaries based on a standard 5% significance level
    is_stationary = p_value < 0.05
    
    conclusion_text = (
        f"Reject H0: The series is stationary (p-value = {p_value:.4f})."
        if is_stationary else
        f"Fail to Reject H0: The series is non-stationary and contains a unit root (p-value = {p_value:.4f})."
    )
    
    return {
        "test_statistic": test_statistic,
        "p_value": p_value,
        "lags_used": lags_used,
        "observations_count": n_obs,
        "critical_values": critical_values,
        "is_stationary": is_stationary,
        "conclusion": conclusion_text,
        "clean_series": clean_series
    }


def plot_stationarity_diagnostics(
    adf_results: dict,
    title_prefix: str = "Time Series",
    save_path: str = None
) -> None:
    """
    Generates a professional 2-panel diagnostic visualization plot. 
    The top panel displays the raw data overlaid with its global mean, and the bottom 
    panel shows the first-differenced series to help evaluate transformations.
    
    Parameters:
    -----------
    adf_results : dict
        The output metric summary dictionary returned from run_adf_stationarity_test.
    title_prefix : str, default='Time Series'
        Descriptive name of the target variable for plot headers.
    save_path : str, optional
        File system destination path to save the completed figure file.
    """
    clean_series = adf_results["clean_series"]
    is_stat = adf_results["is_stationary"]
    p_val = adf_results["p_value"]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Top Panel: Raw Series Data
    status_label = "Stationary" if is_stat else "Non-Stationary"
    ax1.plot(clean_series.index, clean_series.values, color="#2b5c8f", linewidth=1.5, label="Observed")
    ax1.axhline(clean_series.mean(), color="#e31a1c", linestyle="--", linewidth=1.5, label=f"Global Mean ({clean_series.mean():.2f})")
    ax1.set_title(f"{title_prefix} - Raw Sequence [Status: {status_label} | p-val: {p_val:.4f}]", fontsize=12, fontweight="bold", loc="left")
    ax1.set_ylabel("Metric Values", fontsize=11)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left", frameon=True, facecolor="white")
    
    # Bottom Panel: First-Differenced Sequence (The standard stationarity transformation)
    differenced_values = clean_series.diff().dropna()
    ax2.plot(differenced_values.index, differenced_values.values, color="#2ca02c", linewidth=1.2, label="First-Difference (ΔY_t)")
    ax2.axhline(differenced_values.mean(), color="black", linestyle=":", linewidth=1, alpha=0.7)
    ax2.set_title(f"{title_prefix} - First-Differenced Transformation (ΔY_t = Y_t - Y_t-1)", fontsize=11, fontweight="bold", loc="left")
    ax2.set_ylabel("Delta Changes", fontsize=11)
    ax2.set_xlabel("Chronological Index", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper left", frameon=True, facecolor="white")
    
    sns.despine(ax=ax1)
    sns.despine(ax=ax2)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with synthetically generated data to verify functionality
    np.random.seed(42)
    n_samples = 150
    time_horizon = pd.date_range(start="2024-01-01", periods=n_samples, freq="D")
    
    # 1. Generate a Non-Stationary Random Walk Process (should fail the test)
    random_walk_values = np.cumsum(np.random.normal(0.5, 1.0, size=n_samples))
    non_stationary_series = pd.Series(random_walk_values, index=time_horizon, name="Random_Walk")
    
    # 2. Generate a Stationary Autoregressive Process (should pass the test)
    stationary_values = np.zeros(n_samples)
    for t in range(1, n_samples):
        stationary_values[t] = 0.65 * stationary_values[t-1] + np.random.normal(0, 1.0)
    stationary_series = pd.Series(stationary_values, index=time_horizon, name="Stationary_AR1")
    
    print("--- 1. Evaluating Non-Stationary Random Walk Sequence ---")
    rw_results = run_adf_stationarity_test(non_stationary_series, regression_type="c")
    print(f"ADF Statistic: {rw_results['test_statistic']:.4f}")
    print(f"Conclusion: {rw_results['conclusion']}")
    print("Critical Thresholds:")
    for key, val in rw_results["critical_values"].items():
        print(f"   {key}: {val:.4f}")
        
    print("
--- 2. Evaluating Stationary AR(1) Sequence ---")
    ar_results = run_adf_stationarity_test(stationary_series, regression_type="c")
    print(f"ADF Statistic: {ar_results['test_statistic']:.4f}")
    print(f"Conclusion: {ar_results['conclusion']}")
    
    print("
--- 3. Launching Diagnostic Visualizations for the Non-Stationary Series ---")
    plot_stationarity_diagnostics(rw_results, title_prefix="Simulated Growth Asset")
"""
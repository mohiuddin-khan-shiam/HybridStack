"""
Autocorrelation & Partial Autocorrelation Analysis Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on time series sequences using Autocorrelation Functions (ACF) 
and Partial Autocorrelation Functions (PACF). It checks for data completeness, handles
optional differencing to manage trends, and generates clean diagnostic plots with 
statistical confidence bands to identify underlying data structures independent of 
specific datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def prepare_series_for_correlation(
    series: pd.Series, 
    difference_order: int = 0
) -> pd.Series:
    """
    Cleans missing data from the sequence and applies optional differencing transformations
    to ensure data stationarity before analysis.
    
    Parameters:
    -----------
    series : pd.Series
        The input numerical time series or chronological sequence.
    difference_order : int, default=0
        The number of differencing operations to apply (e.g., 1 for Y_t - Y_{t-1}).
        
    Returns:
    --------
    pd.Series
        A processed, clean time series ready for correlation analysis.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("Input 'series' must be a pandas Series object.")
        
    # Clean internal missing values using forward/backward fills
    clean_series = series.dropna()
    
    # Apply differencing if specified to stabilize trends
    if difference_order > 0:
        for _ in range(difference_order):
            clean_series = clean_series.diff()
        clean_series = clean_series.dropna()
        
    return clean_series


def plot_autocorrelation_diagnostic(
    series: pd.Series,
    lags: int = 40,
    title_prefix: str = "Series",
    difference_order: int = 0,
    save_path: str = None
) -> None:
    """
    Generates a professional 2-panel stacked layout displaying the 
    Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF) subplots.
    
    Parameters:
    -----------
    series : pd.Series
        The numerical sequence or time series column to analyze.
    lags : int, default=40
        The maximum number of lag intervals to calculate and display.
    title_prefix : str, default="Series"
        Descriptive name of the target variable for plot headers.
    difference_order : int, default=0
        The differencing step parameter to stabilize trend baselines.
    save_path : str, optional
        File system destination path to save the completed figure file.
    """
    # Preprocess the input data
    processed_series = prepare_series_for_correlation(series, difference_order=difference_order)
    
    # Restrict lag limits if the dataset is too small
    max_allowable_lags = min(lags, len(processed_series) // 2 - 1)
    if max_allowable_lags < lags:
        print(f"Warning: Lookback lags truncated from {lags} to {max_allowable_lags} due to sample size bounds.")
        lags = max_allowable_lags

    # Initialize a clean, stacked subplot layout
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Define a clear label prefix based on transformations applied
    transform_label = f" (Diff Order {difference_order})" if difference_order > 0 else ""
    
    # 1. Render the Autocorrelation Function (ACF) Plot
    plot_acf(
        processed_series, 
        lags=lags, 
        ax=axes[0], 
        color="#2b5c8f", 
        vlines_kwargs={"colors": "#2b5c8f", "linewidth": 1.5},
        alpha=0.05  # Standard 95% Confidence Level
    )
    axes[0].set_title(f"{title_prefix} - Autocorrelation Function (ACF){transform_label}", fontsize=12, fontweight="bold", loc="left")
    axes[0].grid(True, linestyle=":", alpha=0.5)
    
    # 2. Render the Partial Autocorrelation Function (PACF) Plot
    plot_pacf(
        processed_series, 
        lags=lags, 
        ax=axes[1], 
        color="#d95f02", 
        vlines_kwargs={"colors": "#d95f02", "linewidth": 1.5},
        alpha=0.05,
        method="yule_walker"
    )
    axes[1].set_title(f"{title_prefix} - Partial Autocorrelation Function (PACF){transform_label}", fontsize=12, fontweight="bold", loc="left")
    axes[1].grid(True, linestyle=":", alpha=0.5)
    
    plt.xlabel("Lag Horizon Intervals", fontsize=11)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    # Example usage with synthetically generated data to verify functionality
    np.random.seed(42)
    n_samples = 150
    
    # 1. Simulate an Autoregressive Process of Order 2: AR(2)
    # Target signature: ACF should decay slowly; PACF should cut off cleanly after lag 2
    ar2_values = np.zeros(n_samples)
    for t in range(2, n_samples):
        ar2_values[t] = 0.6 * ar2_values[t-1] - 0.25 * ar2_values[t-2] + np.random.normal(0, 1.0)
    ar2_series = pd.Series(ar2_values, name="Synthetic_AR2")
    
    # 2. Simulate a Non-Stationary Trend process
    trend_values = np.linspace(10, 50, n_samples) + np.random.normal(0, 2.0, size=n_samples)
    trend_series = pd.Series(trend_values, name="Synthetic_Trend")
    
    print("--- 1. Processing Stationary Autoregressive AR(2) Sequence ---")
    plot_autocorrelation_diagnostic(ar2_series, lags=30, title_prefix="Simulated AR(2) Process")
    
    print("
--- 2. Processing Non-Stationary Trend Sequence (Raw vs. Differenced) ---")
    # Raw processing shows an artificial trend signature
    plot_autocorrelation_diagnostic(trend_series, lags=30, title_prefix="Simulated Trend (Raw)")
    # Applying a first-difference removes the trend to reveal internal patterns
    plot_autocorrelation_diagnostic(trend_series, lags=30, title_prefix="Simulated Trend (Differenced)", difference_order=1)
"""
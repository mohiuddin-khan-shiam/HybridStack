"""
Time Series Decomposition Analysis & Structural Component Profiling Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on chronological time series data. It specializes in breaking down
observed variables into distinct trend-cycle, seasonal, and irregular residual components 
using classical additive or multiplicative decomposition models, checking data consistency, 
and outputting professional diagnostic metrics and visualizations.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf


def validate_and_prepare_series(df: pd.DataFrame, target_col: str, fill_method: str = "interpolate") -> pd.Series:
    """
    Validates that the input DataFrame has a proper DatetimeIndex, ensures continuous 
    frequency alignment, and manages internal null or missing entries.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame containing the target time series column.
    target_col : str
        The name of the target numerical column to analyze.
    fill_method : str, default="interpolate"
        The technique used to handle missing data gaps ('interpolate', 'ffill', 'bfill').
        
    Returns:
    --------
    pd.Series
        A clean, continuous time series with a validated index and no missing values.
    """
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame index must be a valid pandas DatetimeIndex.")
        
    series = df[target_col].copy()
    
    # Inferred frequency adjustment if missing
    if series.index.freq is None:
        inferred_freq = pd.infer_freq(series.index)
        if inferred_freq:
            series = series.asfreq(inferred_freq)
            
    # Missing data management
    if series.isnull().any():
        if fill_method == "interpolate":
            series = series.interpolate(method="time")
        elif fill_method == "ffill":
            series = series.ffill()
        elif fill_method == "bfill":
            series = series.bfill()
            
    # Drop any remaining boundary NaNs that couldn't be filled
    series = series.dropna()
    return series


def perform_time_series_decomposition(
    series: pd.Series, 
    model_type: str = "additive", 
    period: int = 12
) -> dict:
    """
    Decomposes a time series into observed, trend, seasonal, and residual elements.
    
    Parameters:
    -----------
    series : pd.Series
        Clean time series sequence with a defined frequency.
    model_type : str, default="additive"
        The type of decomposition model to fit ('additive' or 'multiplicative').
    period : int, default=12
        The seasonal period frequency (e.g., 12 for monthly, 4 for quarterly).
        
    Returns:
    --------
    dict
        A dictionary containing the decomposition components and structural metadata.
    """
    if len(series) < (2 * period):
        raise ValueError(f"Series length ({len(series)}) must be at least twice the seasonal period ({2 * period}).")
        
    decomposition = seasonal_decompose(series, model=model_type, period=period)
    
    return {
        "model_type": model_type,
        "period": period,
        "observed": decomposition.observed,
        "trend": decomposition.trend,
        "seasonal": decomposition.seasonal,
        "resid": decomposition.resid,
        "raw_object": decomposition
    }


def plot_decomposition_components(
    decomp_results: dict, 
    title_prefix: str = "Time Series Component", 
    save_path: str = None
) -> None:
    """
    Generates a professional 4-panel stacked visualization displaying the 
    Observed, Trend, Seasonal, and Residual components.
    
    Parameters:
    -----------
    decomp_results : dict
        The output dictionary from perform_time_series_decomposition.
    title_prefix : str, default="Time Series Component"
        The descriptive name prefix of the target feature being reviewed.
    save_path : str, optional
        File path to save the generated figure.
    """
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    model_label = decomp_results["model_type"].capitalize()
    
    # Define cohesive professional color palettes
    colors = ["#2b5c8f", "#d95f02", "#2ca02c", "#e31a1c"]
    components = ["observed", "trend", "seasonal", "resid"]
    labels = ["Observed Data", "Long-Term Trend", f"Seasonal Wave ({model_label})", "Irregular Residuals"]
    
    for i, comp in enumerate(components):
        axes[i].plot(decomp_results[comp], color=colors[i], linewidth=1.5, label=labels[i])
        axes[i].set_title(f"{title_prefix} - {labels[i]}", fontsize=11, fontweight="bold", loc="left")
        axes[i].grid(True, linestyle=":", alpha=0.6)
        axes[i].legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")
        
        # Style adjustments specific to residual scatter verification
        if comp == "resid":
            axes[i].axhline(0 if decomp_results["model_type"] == "additive" else 1, color="grey", linestyle="--", linewidth=1)
            
    plt.xlabel("Timeline Index", fontsize=11)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_residual_diagnostics(decomp_results: dict, save_path: str = None) -> None:
    """
    Generates diagnostic plots for the irregular residual component, including 
    an autocorrelation chart and an error distribution histogram, to check for remaining patterns.
    
    Parameters:
    -----------
    decomp_results : dict
        The output dictionary from perform_time_series_decomposition.
    save_path : str, optional
        File path to save the generated figure.
    """
    residuals = decomp_results["resid"].dropna()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left Plot: Distribution Histogram
    ax1.hist(residuals, bins=25, color="#7570b3", alpha=0.8, edgecolor="black", linewidth=0.5)
    ax1.axvline(residuals.mean(), color="red", linestyle="--", linewidth=1.5, label=f"Mean: {residuals.mean():.4f}")
    ax1.set_title("Residual Error Distribution Profile", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Residual Magnitude")
    ax1.set_ylabel("Frequency Count")
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend()
    
    # Right Plot: Autocorrelation (ACF) chart to check for systematic patterns
    plot_acf(residuals, ax=ax2, lags=min(decomp_results["period"] * 2, len(residuals) // 3), color="#1f78b4")
    ax2.set_title("Residual Autocorrelation Function (ACF)", fontsize=12, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.5)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with a synthetically generated time series dataset to verify functionality
    np.random.seed(42)
    time_index = pd.date_range(start="2018-01-01", periods=60, freq="M")
    
    # Construct a synthetic dataset with a clear upward trend and annual seasonality
    trend_cycle = 100.0 + (1.5 * np.arange(60))
    seasonal_pattern = 10.0 * np.sin(2 * np.pi * np.arange(60) / 12)
    stochastic_noise = np.random.normal(0, 2.5, size=60)
    observed_values = trend_cycle + seasonal_pattern + stochastic_noise
    
    mock_df = pd.DataFrame({
        "Simulated_Metric": observed_values
    }, index=time_index)
    
    print("--- 1. Data Pipeline Validation & Alignment ---")
    clean_series = validate_and_prepare_series(mock_df, target_col="Simulated_Metric")
    print(f"Data validated successfully. Total data points: {len(clean_series)}")
    
    print("
--- 2. Computing Time Series Decomposition ---")
    results = perform_time_series_decomposition(clean_series, model_type="additive", period=12)
    print("Decomposition completed. Structural components isolated.")
    
    print("
--- 3. Generating Visualization Grids ---")
    plot_decomposition_components(results, title_prefix="Simulated Metric")
    plot_residual_diagnostics(results)
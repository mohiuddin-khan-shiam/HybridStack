"""
Time Series Resampling & Frequency Interpolation Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) and data preprocessing to modify time series sampling frequencies.
It handles pandas DatetimeIndex validation, executes downsampling aggregations, performs
upsampling expansions, and fits multiple interpolation models (linear, time-weighted, spline)
while generating clear, publication-grade diagnostic plots independent of specific datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def transform_series_frequency(
    series: pd.Series,
    target_frequency: str,
    operation_type: str = "downsample",
    downsample_agg: str = "mean",
    interpolation_method: str = "linear",
    spline_order: int = 3
) -> pd.Series:
    """
    Modifies the frequency of a time series through downsampling aggregation or 
    upsampling expansion with mathematical interpolation.
    
    Parameters:
    -----------
    series : pd.Series
        The input time series featuring a valid pandas DatetimeIndex.
    target_frequency : str
        The target frequency alias (e.g., 'D' for daily, 'M' for monthly, 'YE' for yearly).
    operation_type : str, default='downsample'
        The modification path to execute: 'downsample' or 'upsample'.
    downsample_agg : str, default='mean'
        The aggregation operator used for downsampling ('mean', 'sum', 'median', 'first', 'last').
    interpolation_method : str, default='linear'
        The interpolation technique used for upsampling ('linear', 'time', 'cubic', 'spline', 'ffill', 'bfill').
    spline_order : int, default=3
        The polynomial degree applied if interpolation_method is set to 'spline'.
        
    Returns:
    --------
    pd.Series
        A new transformed time series formatted to the target frequency scale.
    """
    if not isinstance(series.index, pd.DatetimeIndex):
        raise ValueError("The input series index must be a valid pandas DatetimeIndex.")
        
    clean_series = series.dropna()
    if clean_series.empty:
        raise ValueError("The input time series sequence is empty after removing missing entries.")
        
    # Instantiate the base resampler object
    resampler = clean_series.resample(target_frequency)
    
    if operation_type == "downsample":
        # Apply the chosen statistical aggregator
        if downsample_agg == "mean":
            return resampler.mean()
        elif downsample_agg == "sum":
            return resampler.sum()
        elif downsample_agg == "median":
            return resampler.median()
        elif downsample_agg == "first":
            return resampler.first()
        elif downsample_agg == "last":
            return resampler.last()
        else:
            raise ValueError(f"Unsupported downsampling aggregator: {downsample_agg}")
            
    elif operation_type == "upsample":
        # First re-index the series to the higher frequency framework
        resampled_base = resampler.asfreq()
        
        # Apply the chosen numerical interpolation model
        if interpolation_method in ["ffill", "pad"]:
            return resampled_base.ffill()
        elif interpolation_method == "bfill":
            return resampled_base.bfill()
        elif interpolation_method in ["linear", "time"]:
            return resampled_base.interpolate(method=interpolation_method)
        elif interpolation_method in ["cubic", "spline"]:
            kwargs = {"order": spline_order} if interpolation_method == "spline" else {}
            return resampled_base.interpolate(method=interpolation_method, **kwargs)
        else:
            raise ValueError(f"Unsupported interpolation method: {interpolation_method}")
            
    else:
        raise ValueError(f"Unsupported operation_type: {operation_type}. Choose 'downsample' or 'upsample'.")


def plot_resampling_diagnostic(
    original: pd.Series,
    downsampled: pd.Series,
    upsampled: pd.Series,
    title_prefix: str = "Time Series",
    y_label: str = "Values",
    save_path: str = None
) -> None:
    """
    Generates a professional, publication-grade visualization grid overlaying the 
    original historical data with the downsampled and upsampled frequency tracks.
    
    Parameters:
    -----------
    original : pd.Series
        The unaltered raw input time series.
    downsampled : pd.Series
        The compressed, lower-frequency series output.
    upsampled : pd.Series
        The expanded, higher-frequency interpolated series output.
    title_prefix : str, default='Time Series'
        Descriptive name of the target variable for chart headers.
    y_label : str, default='Values'
        Text label for the vertical coordinate axis.
    save_path : str, optional
        File system destination path to save the completed figure file.
    """
    plt.figure(figsize=(13, 6.5))
    sns.set_theme(style="ticks")
    
    # Render the original data with partial transparency to keep the plot readable
    plt.plot(original.index, original.values, label="Original Reference Data", color="#1f78b4", alpha=0.35, linewidth=1.2)
    
    # Overlay the downsampled aggregation path
    plt.plot(downsampled.index, downsampled.values, marker="o", markersize=5, linestyle="-", 
             color="#e31a1c", linewidth=2.0, label=f"Downsampled Curve")
             
    # Overlay the upsampled interpolated path
    plt.plot(upsampled.index, upsampled.values, linestyle="--", 
             color="#2ca02c", linewidth=1.5, label=f"Upsampled Interpolated Curve")
             
    plt.title(f"{title_prefix}: Frequency Resampling & Interpolation Alignment Profile", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Chronological Timeline Index", fontsize=11, labelpad=8)
    plt.ylabel(y_label, fontsize=11, labelpad=8)
    
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")
    
    sns.despine()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with synthetically generated data to verify functionality
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    np.random.seed(42)
    n_months = 48
    time_index = pd.date_range(start="2022-01-01", periods=n_months, freq="ME")
    
    # Construct a synthetic monthly dataset with an upward trend and seasonal oscillations
    underlying_growth = np.linspace(12, 35, n_months)
    seasonal_swings = 4.0 * np.sin(2 * np.pi * np.arange(n_months) / 12)
    stochastic_noise = np.random.normal(0, 0.8, size=n_months)
    
    mock_values = underlying_growth + seasonal_swings + stochastic_noise
    mock_series = pd.Series(mock_values, index=time_index, name="Simulated_Rate")
    
    print("--- 1. Processing Downsampling Operations (Monthly to Yearly) ---")
    yearly_aggregated = transform_series_frequency(
        series=mock_series,
        target_frequency="Y",
        operation_type="downsample",
        downsample_agg="mean"
    )
    print("Downsampled output summary:")
    print(yearly_aggregated)
    
    print("
--- 2. Processing Upsampling Operations (Yearly back to Monthly via Spline) ---")
    # Upsample the yearly data back to monthly intervals using a smooth cubic spline interpolation
    monthly_interpolated = transform_series_frequency(
        series=yearly_aggregated,
        target_frequency="ME",
        operation_type="upsample",
        interpolation_method="cubic"
    )
    print("
Upsampled interpolated preview:")
    print(monthly_interpolated.head(8))
    
    print("
--- 3. Launching Frequency Overlay Visualizations ---")
    plot_resampling_diagnostic(
        original=mock_series,
        downsampled=yearly_aggregated,
        upsampled=monthly_interpolated,
        title_prefix="Simulated Macroeconomic Indicator",
        y_label="Index Percentage Values"
    )
"""
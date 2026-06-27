"""
Rolling Window Analysis & Statistical Smoothing Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on time series sequences using rolling windows. It handles calculation
pipelines for Simple Moving Averages (SMA), Exponential Moving Averages (EMA), rolling 
standard deviations, and dynamic volatility bands, outputting high-quality visualizations 
independent of specific project datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calculate_rolling_statistics(
    series: pd.Series, 
    window: int = 12, 
    min_periods: int = None
) -> pd.DataFrame:
    """
    Computes a core suite of rolling statistics for a given time series.
    
    Parameters:
    -----------
    series : pd.Series
        The chronological numerical time series to analyze.
    window : int, default=12
        The size of the moving lookback window.
    min_periods : int, optional
        Minimum number of observations in window required to have a value.
        Defaults to the window size if not specified.
        
    Returns:
    --------
    pd.DataFrame
        A DataFrame containing the raw series alongside its rolling metrics 
        (SMA, EMA, rolling standard deviation, and volatility envelopes).
    """
    if not isinstance(series, pd.Series):
        raise TypeError("Input 'series' must be a pandas Series object.")
    if window <= 0:
        raise ValueError("Window size must be a positive integer greater than zero.")
        
    if min_periods is None:
        min_periods = window

    results_df = pd.DataFrame(index=series.index)
    results_df["Observed"] = series
    
    # Calculate rolling central tendencies
    results_df["SMA"] = series.rolling(window=window, min_periods=min_periods).mean()
    results_df["EMA"] = series.ewm(span=window, adjust=False, min_periods=min_periods).mean()
    
    # Calculate rolling volatility and dispersion
    results_df["Rolling_Std"] = series.rolling(window=window, min_periods=min_periods).std()
    
    # Formulate structural volatility bands (2 Standard Deviations)
    results_df["Upper_Band"] = results_df["SMA"] + (2 * results_df["Rolling_Std"])
    results_df["Lower_Band"] = results_df["SMA"] - (2 * results_df["Rolling_Std"])
    
    return results_df


def plot_rolling_smoothing(
    metrics_df: pd.DataFrame, 
    title_prefix: str = "Time Series", 
    save_path: str = None
) -> None:
    """
    Plots the observed series alongside its smoothed SMA and EMA representations 
    to analyze trend adjustments and lookback lag.
    
    Parameters:
    -----------
    metrics_df : pd.DataFrame
        DataFrame output from calculate_rolling_statistics.
    title_prefix : str, default="Time Series"
        Descriptive name of the variable under analysis.
    save_path : str, optional
        File path to save the generated figure.
    """
    plt.figure(figsize=(12, 6))
    
    # Plot raw observed data with subtle transparency to highlight trend indicators
    plt.plot(metrics_df.index, metrics_df["Observed"], label="Observed", color="#1f78b4", alpha=0.35, linewidth=1.2)
    
    # Plot smoothed indicators
    plt.plot(metrics_df.index, metrics_df["SMA"], label="Simple Moving Avg (SMA)", color="#e31a1c", alpha=0.9, linewidth=2)
    plt.plot(metrics_df.index, metrics_df["EMA"], label="Exponential Moving Avg (EMA)", color="#2ca02c", alpha=0.9, linewidth=1.5, linestyle="--")
    
    plt.title(f"{title_prefix}: Trend Smoothing Profile", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Chronological Index", fontsize=11)
    plt.ylabel("Value Metrics", fontsize=11)
    
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_volatility_envelopes(
    metrics_df: pd.DataFrame, 
    title_prefix: str = "Time Series", 
    save_path: str = None
) -> None:
    """
    Plots the observed data surrounded by dynamic volatility bands 
    to track changes in stability and detect structural regime shifts.
    
    Parameters:
    -----------
    metrics_df : pd.DataFrame
        DataFrame output from calculate_rolling_statistics.
    title_prefix : str, default="Time Series"
        Descriptive name of the variable under analysis.
    save_path : str, optional
        File path to save the generated figure.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    
    # Upper Plot: Central Trend and Volatility Bands
    ax1.plot(metrics_df.index, metrics_df["Observed"], label="Observed", color="#2b5c8f", alpha=0.4, linewidth=1)
    ax1.plot(metrics_df.index, metrics_df["SMA"], label="SMA Baseline", color="#d95f02", linewidth=1.5)
    ax1.plot(metrics_df.index, metrics_df["Upper_Band"], label="Volatility Bands (±2σ)", color="#7570b3", linestyle=":", alpha=0.8)
    ax1.plot(metrics_df.index, metrics_df["Lower_Band"], color="#7570b3", linestyle=":", alpha=0.8)
    
    # Fill variance region
    ax1.fill_between(metrics_df.index, metrics_df["Lower_Band"], metrics_df["Upper_Band"], color="#7570b3", alpha=0.1)
    
    ax1.set_title(f"{title_prefix}: Dynamic Volatility Bands", fontsize=12, fontweight="bold")
    ax1.set_ylabel("Value Metrics", fontsize=11)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.legend(loc="upper left")
    
    # Lower Plot: Isolated Standard Deviation
    ax2.plot(metrics_df.index, metrics_df["Rolling_Std"], label="Rolling Std Dev (Volatility)", color="#e31a1c", linewidth=1.5)
    ax2.set_ylabel("Standard Deviation", fontsize=11)
    ax2.set_xlabel("Chronological Index", fontsize=11)
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper left")
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with synthetically generated data to verify functionality
    np.random.seed(42)
    time_index = pd.date_range(start="2020-01-01", periods=150, freq="M")
    
    # Generate a time series with a structural trend change and a high-volatility regime
    base_trend = np.linspace(50, 120, 150)
    seasonal_noise = 8 * np.sin(2 * np.pi * np.arange(150) / 12)
    
    # Introduce a specific high-volatility shock regime mid-series
    random_shocks = np.random.normal(0, 3, size=150)
    random_shocks[60:90] = np.random.normal(0, 12, size=30) 
    
    mock_series = pd.Series(base_trend + seasonal_noise + random_shocks, index=time_index)
    
    print("--- 1. Processing Rolling Computations (Window=12) ---")
    rolling_metrics = calculate_rolling_statistics(mock_series, window=12)
    print(rolling_metrics[["Observed", "SMA", "EMA", "Rolling_Std"]].tail())
    
    print("
--- 2. Generating Trend Smoothing Visualization ---")
    plot_rolling_smoothing(rolling_metrics, title_prefix="Simulated Operational Index")
    
    print("
--- 3. Generating Volatility Envelope Visualization ---")
    plot_volatility_envelopes(rolling_metrics, title_prefix="Simulated Operational Index")
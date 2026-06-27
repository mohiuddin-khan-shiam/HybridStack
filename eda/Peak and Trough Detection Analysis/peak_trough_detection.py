"""
Peak & Trough Detection Turning Point Extraction Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on time-series sequences to locate local extrema. It automates missing 
data handling, executes neighbor comparison optimization algorithms via scipy, configures 
customizable lookback/lookahead distance constraints, and generates high-quality 
extrema marker plots independent of specific project datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import find_peaks


def detect_local_extrema(
    series: pd.Series,
    min_distance: int = 30,
    prominence: float = None,
    height: float = None
) -> dict:
    """
    Cleans sequential data and identifies the exact index locations of local 
    maxima (peaks) and local minima (troughs) using neighborhood constraints.
    
    Parameters:
    -----------
    series : pd.Series
        The input chronological numerical time series to process.
    min_distance : int, default=30
        The minimum number of data steps required to separate consecutive extrema.
    prominence : float, optional
        The minimum topographical prominence required to retain an extreme point.
    height : float, optional
        The absolute numerical value threshold cut-off required for peaks.
        
    Returns:
    --------
    dict
        A dictionary containing the parsed arrays of peak indices, trough indices, 
        corresponding datetime stamps, and a clean data reference series.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("Input 'series' must be a valid pandas Series object.")
        
    # Clean out internal missing entries using linear time interpolation
    clean_series = series.copy()
    if clean_series.isnull().any():
        clean_series = clean_series.interpolate(method="time")
    clean_series = clean_series.dropna()
    
    if clean_series.empty:
        raise ValueError("The input time series is empty after removing missing entries.")
        
    values_array = clean_series.values
    time_index = clean_series.index
    
    # 1. Locate local maxima (Peaks)
    peak_indices, _ = find_peaks(
        values_array, 
        distance=min_distance, 
        prominence=prominence, 
        height=height
    )
    
    # 2. Locate local minima (Troughs) by negating the sequence values
    # Inverting height thresholds if provided to match the negative space mapping
    trough_height = -height if height is not None else None
    trough_indices, _ = find_peaks(
        -values_array, 
        distance=min_distance, 
        prominence=prominence, 
        height=trough_height
    )
    
    # Map raw integer index arrays back to the corresponding datetime index stamps
    peak_dates = time_index[peak_indices]
    trough_dates = time_index[trough_indices]
    
    return {
        "peak_indices": peak_indices,
        "trough_indices": trough_indices,
        "peak_dates": peak_dates,
        "trough_dates": trough_dates,
        "clean_series": clean_series
    }


def plot_local_extrema_profile(
    extrema_results: dict,
    title_prefix: str = "Time Series",
    y_label: str = "Values",
    save_path: str = None
) -> None:
    """
    Generates a professional, publication-grade time-series visualization plot
    overlaying the continuous data stream with distinct colored point markers 
    highlighting verified peaks and troughs.
    
    Parameters:
    -----------
    extrema_results : dict
        The output metric summary dictionary returned from detect_local_extrema.
    title_prefix : str, default='Time Series'
        Descriptive name of the target variable for chart headers.
    y_label : str, default='Values'
        Text label for the vertical coordinate axis.
    save_path : str, optional
        File system destination path to save the completed figure file.
    """
    clean_series = extrema_results["clean_series"]
    peak_idx = extrema_results["peak_indices"]
    trough_idx = extrema_results["trough_indices"]
    
    plt.figure(figsize=(13, 6.5))
    sns.set_theme(style="ticks")
    
    # Render the continuous raw sequence baseline path
    plt.plot(clean_series.index, clean_series.values, label="Observed Data Path", 
             color="#1f78b4", alpha=0.6, linewidth=1.8)
    
    # Overlay local maxima peaks using red circular markers
    if len(peak_idx) > 0:
        plt.plot(clean_series.index[peak_idx], clean_series.values[peak_idx], 
                 "ro", label=f"Identified Peaks (Count: {len(peak_idx)})", 
                 markersize=7, markeredgecolor="black", markeredgewidth=0.6, zorder=4)
                 
    # Overlay local minima troughs using green circular markers
    if len(trough_idx) > 0:
        plt.plot(clean_series.index[trough_idx], clean_series.values[trough_idx], 
                 "go", label=f"Identified Troughs (Count: {len(trough_idx)})", 
                 markersize=7, markeredgecolor="black", markeredgewidth=0.6, zorder=4)
                 
    plt.title(f"{title_prefix}: Extrema Turning Point Profile (Local Peak/Trough Detection)", fontsize=13, fontweight="bold", pad=15)
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
    np.random.seed(42)
    n_periods = 250
    time_index = pd.date_range(start="2024-01-01", periods=n_periods, freq="D")
    
    # Construct a synthetic daily dataset featuring a cyclical waveform and random noise
    base_signal = np.linspace(50, 75, n_periods)
    cyclical_cycle = 12 * np.sin(2 * np.pi * np.arange(n_periods) / 45)
    stochastic_noise = np.random.normal(0, 1.5, size=n_periods)
    
    mock_values = base_signal + cyclical_cycle + stochastic_noise
    mock_series = pd.Series(mock_values, index=time_index, name="Simulated_Rate")
    
    print("--- 1. Executing Turning Point Detection Pipeline (Distance=30) ---")
    extrema_output = detect_local_extrema(mock_series, min_distance=30, prominence=None, height=None)
    print(f"Calculated Turning Points -> Peaks Found: {len(extrema_output['peak_indices'])} | Troughs Found: {len(extrema_output['trough_indices'])}")
    print("\nSample Discovered Peak Datetime Stamps:")
    print(extrema_output["peak_dates"][:3])
    
    print("
--- 2. Launching Extrema Visualization Overlay ---")
    plot_local_extrema_profile(
        extrema_results=extrema_output,
        title_prefix="Simulated Cyclical Index",
        y_label="Metric Scaling Units"
    )
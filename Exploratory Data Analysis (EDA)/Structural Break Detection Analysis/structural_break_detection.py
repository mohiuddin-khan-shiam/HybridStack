"""
Structural Break Detection & Time-Series Regime Segmentation Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) to detect change-points and structural breaks in time-series data. 
It automates missing data filters, applies segmentation algorithms (such as Binary 
Segmentation) to locate shifts in baseline parameters, computes localized segment 
profiles, and outputs professional, publication-grade visualization grids independent 
of specific project columns.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Safe package integration framework for change-point handling
try:
    import ruptures as rpt
    HAS_RUPTURES = True
except ImportError:
    HAS_RUPTURES = False


def detect_structural_breaks(
    series: pd.Series,
    num_breaks: int = 3,
    model_type: str = "l2",
    min_segment_size: int = 10
) -> dict:
    """
    Executes a Binary Segmentation search across a numerical time-series sequence 
    to pinpoint structural change-point index boundaries.
    
    Parameters:
    -----------
    series : pd.Series
        The input chronological numerical time series.
    num_breaks : int, default=3
        The total number of structural change-points to locate.
    model_type : str, default='l2'
        The segmentation cost model parameter ('l2' for mean shifts, 'rbf' for kernel variance).
    min_segment_size : int, default=10
        The minimum number of data points required to form an isolated segment.
        
    Returns:
    --------
    dict
        A dictionary containing the break indices, exact datetime stamps, 
        and structural metadata summaries for each isolated regime.
    """
    if not HAS_RUPTURES:
        raise ModuleNotFoundError(
            "The 'ruptures' package is missing. Install it using 'pip install ruptures' "
            "to enable structural break detection tools."
        )
        
    # Clean out missing records from the series pipeline
    clean_series = series.dropna()
    if clean_series.empty:
        raise ValueError("The input time series series contains no valid numerical entries.")
        
    values_array = clean_series.values
    time_index = clean_series.index
    
    # Initialize and execute the Binary Segmentation search algorithm
    algo = rpt.Binseg(model=model_type, min_size=min_segment_size)
    algo.fit(values_array)
    
    # Predict returns the endpoints of the segments (including the last array index)
    predicted_endpoints = algo.predict(n_bkps=num_breaks)
    
    # Isolate the interior break points by dropping the final entry
    break_indices = predicted_endpoints[:-1]
    break_dates = [time_index[idx] for idx in break_indices]
    
    # Group data into segments to calculate localized metrics
    segments_summary = []
    start_idx = 0
    
    for k, end_idx in enumerate(predicted_endpoints):
        segment_data = values_array[start_idx:end_idx]
        segment_dates = time_index[start_idx:min(end_idx, len(time_index)-1)]
        
        segments_summary.append({
            "Segment_ID": k + 1,
            "Start_Index": start_idx,
            "End_Index": end_idx,
            "Start_Date": time_index[start_idx],
            "End_Date": time_index[min(end_idx - 1, len(time_index) - 1)],
            "Count": len(segment_data),
            "Mean": np.mean(segment_data) if len(segment_data) > 0 else np.nan,
            "Std_Dev": np.std(segment_data) if len(segment_data) > 0 else np.nan
        })
        start_idx = end_idx
        
    return {
        "break_indices": break_indices,
        "break_dates": break_dates,
        "segments": pd.DataFrame(segments_summary),
        "clean_series": clean_series
    }


def plot_structural_breaks(
    break_results: dict,
    title_prefix: str = "Time Series",
    y_label: str = "Values",
    save_path: str = None
) -> None:
    """
    Generates a professional time plot overlaying the raw sequence with vertical 
    change-point indicators and step-like lines showing each segment's average value.
    
    Parameters:
    -----------
    break_results : dict
        The metric summary dictionary returned from detect_structural_breaks.
    title_prefix : str, default="Time Series"
        Descriptive name of the target feature being evaluated.
    y_label : str, default="Values"
        Text label for the vertical coordinate axis.
    save_path : str, optional
        File system destination path to save the completed figure file.
    """
    clean_series = break_results["clean_series"]
    break_dates = break_results["break_dates"]
    segments_df = break_results["segments"]
    
    plt.figure(figsize=(13, 6.5))
    
    # Plot the raw observed series data
    plt.plot(clean_series.index, clean_series.values, color="#2b5c8f", alpha=0.5, linewidth=1.5, label="Observed Data")
    
    # Overlay step lines showing the average value within each segment
    for _, row in segments_df.iterrows():
        plt.hlines(
            y=row["Mean"],
            xmin=row["Start_Date"],
            xmax=row["End_Date"],
            colors="#e31a1c",
            linewidth=2.5,
            linestyle="-",
            zorder=3,
            label="Segment Mean" if row["Segment_ID"] == 1 else ""
        )
        
    # Draw vertical lines at each detected structural break point
    for idx, break_date in enumerate(break_dates):
        plt.axvline(
            break_date,
            color="black",
            linestyle="--",
            linewidth=1.5,
            alpha=0.85,
            zorder=4,
            label="Structural Break" if idx == 0 else ""
        )
        
    plt.title(f"{title_prefix}: Structural Break & Regime Segmentation Analysis", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Chronological Timeline Index", fontsize=11, labelpad=8)
    plt.ylabel(y_label, fontsize=11, labelpad=8)
    
    plt.grid(True, linestyle=":", alpha=0.4)
    plt.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with a synthetically generated time series dataset to verify functionality
    # Mocking structural regime changes requires the ruptures library to be present
    if not HAS_RUPTURES:
        print("Notice: installing 'ruptures' to run the structural break validation execution pipeline...")
        os.system("pip install ruptures")
        import ruptures as rpt
        
    np.random.seed(42)
    time_horizon = pd.date_range(start="2016-01-01", periods=160, freq="M")
    
    # Construct three distinct statistical regimes (mean shifts) to verify detection accuracy
    regime_1 = np.random.normal(15.0, 1.2, size=50)   # Era 1 Mean: 15.0
    regime_2 = np.random.normal(28.0, 1.5, size=60)   # Era 2 Mean: 28.0 (Abrupt shift up)
    regime_3 = np.random.normal(10.0, 1.0, size=50)   # Era 3 Mean: 10.0 (Abrupt drop down)
    
    mock_values = np.concatenate([regime_1, regime_2, regime_3])
    mock_df = pd.DataFrame({"Simulated_Indicator": mock_values}, index=time_horizon)
    
    print("--- 1. Running Structural Change-Point Detection Pipeline ---")
    # Execute the segmentation search to find the 2 internal breakpoints separating our 3 regimes
    break_output = detect_structural_breaks(
        series=mock_df["Simulated_Indicator"],
        num_breaks=2,
        model_type="l2",
        min_segment_size=15
    )
    
    print("
--- 2. Discovered Regime Transitions Summary Table ---")
    print(break_output["segments"].to_string(index=False))
    
    print("
--- 3. Launching Structural Break Time-Series Visualization ---")
    plot_structural_breaks(
        break_results=break_output,
        title_prefix="Simulated Operational Index",
        y_label="Index Metric Units"
    )
"""
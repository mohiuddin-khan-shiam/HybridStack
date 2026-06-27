"""
Dynamic Time Warping (DTW) Shape Alignment & Distance Engine

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on time-series pairs using Dynamic Time Warping. It automates individual 
Z-score standardization, populates bivariate local cost matrices, solves optimal warping paths 
via dynamic programming, and generates high-quality diagnostic visualizations to analyze 
temporal stretching, compression, and lead-lag dynamics independent of specific datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist


def calculate_dtw_matrices(x: np.ndarray, y: np.ndarray) -> dict:
    """
    Computes the local cost matrix, the accumulated cost matrix via dynamic 
    programming, and backtracks to locate the optimal warping path.
    
    Parameters:
    -----------
    x : np.ndarray
        First numerical sequence array (Length N).
    y : np.ndarray
        Second numerical sequence array (Length M).
        
    Returns:
    --------
    dict
        A dictionary containing the accumulated cost matrix, the sorted list of 
        coordinates representing the optimal warping path, and the normalized DTW distance.
    """
    # Enforce flat 1D arrays and clean out any missing data values
    x_clean = np.asarray(x, dtype=float).flatten()
    y_clean = np.asarray(y, dtype=float).flatten()
    
    x_clean = x_clean[~np.isnan(x_clean)]
    y_clean = y_clean[~np.isnan(y_clean)]
    
    N, M = len(x_clean), len(y_clean)
    if N == 0 or M == 0:
        raise ValueError("Input series arrays must contain valid, non-null numerical entries.")
        
    # Standardize both arrays individually using Z-score scaling
    # This ensures the DTW cost measures structural shape rather than scale offsets
    x_std = (x_clean - x_clean.mean()) / (x_clean.std() if x_clean.std() > 0 else 1.0)
    y_std = (y_clean - y_clean.mean()) / (y_clean.std() if y_clean.std() > 0 else 1.0)
    
    # 1. Compute the local cost matrix (Squared Euclidean Distance)
    local_cost = cdist(x_std.reshape(-1, 1), y_std.reshape(-1, 1), metric='sqeuclidean')
    
    # 2. Populate the Accumulated Cost Matrix using dynamic programming rules
    accumulated_cost = np.zeros((N, M))
    accumulated_cost[0, 0] = local_cost[0, 0]
    
    # Initialize boundaries
    for i in range(1, N):
        accumulated_cost[i, 0] = accumulated_cost[i-1, 0] + local_cost[i, 0]
    for j in range(1, M):
        accumulated_cost[0, j] = accumulated_cost[0, j-1] + local_cost[0, j]
        
    # Propagate values through the remaining grid cells
    for i in range(1, N):
        for j in range(1, M):
            accumulated_cost[i, j] = local_cost[i, j] + min(
                accumulated_cost[i-1, j],    # Temporal compression
                accumulated_cost[i, j-1],    # Temporal stretching
                accumulated_cost[i-1, j-1]   # Synchronous step
            )
            
    # 3. Backtrack from cell (N-1, M-1) to find the optimal path
    i, j = N - 1, M - 1
    path = [(i, j)]
    
    while i > 0 or j > 0:
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            # Find the predecessor cell with the lowest accumulated cost
            steps = [accumulated_cost[i-1, j-1], accumulated_cost[i-1, j], accumulated_cost[i, j-1]]
            best_step = np.argmin(steps)
            if best_step == 0:
                i, j = i - 1, j - 1
            elif best_step == 1:
                i -= 1
            else:
                j -= 1
        path.append((i, j))
        
    # Reverse path to start chronologically from index (0,0)
    path.reverse()
    path_array = np.array(path)
    
    # Normalize the total distance score by the path length
    dtw_distance = accumulated_cost[N-1, M-1] / len(path)
    
    return {
        "accumulated_cost": accumulated_cost,
        "path": path_array,
        "distance": dtw_distance,
        "x_normalized": x_std,
        "y_normalized": y_std
    }


def plot_dtw_alignment_grid(dtw_results: dict, x_name: str = "Series X", y_name: str = "Series Y") -> None:
    """
    Plots the accumulated cost matrix heatmap with the optimal warping path 
    overlaid to show the temporal alignment dynamics.
    
    Parameters:
    -----------
    dtw_results : dict
        The output dictionary from calculate_dtw_matrices.
    x_name : str, default="Series X"
        Descriptive label for the horizontal time series variable.
    y_name : str, default="Series Y"
        Descriptive label for the vertical time series variable.
    """
    acc_cost = dtw_results["accumulated_cost"]
    path = dtw_results["path"]
    
    plt.figure(figsize=(9, 7))
    
    # Render the accumulated cost matrix as a background heatmap
    plt.imshow(acc_cost, aspect='auto', cmap='coolwarm', origin='lower')
    plt.colorbar(label="Accumulated Cost Magnitude")
    
    # Overlay the optimal warping path
    plt.plot(path[:, 1], path[:, 0], color="#2ca02c", linewidth=3.0, label="Optimal Warping Path")
    
    # Draw a reference diagonal line to highlight lead-lag variations
    plt.plot([0, acc_cost.shape[1]-1], [0, acc_cost.shape[0]-1], color="black", linestyle=":", alpha=0.6, label="Perfect Sync Line")
    
    plt.title(f"DTW Accumulated Cost Matrix\nShape Distance: {dtw_results['distance']:.4f}", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel(f"Time Step Indices ({x_name})", fontsize=11)
    plt.ylabel(f"Time Step Indices ({y_name})", fontsize=11)
    plt.legend(loc="upper left", frameon=True, facecolor="white")
    plt.tight_layout()
    plt.show()


def plot_dtw_connected_lines(dtw_results: dict, x_name: str = "Series X", y_name: str = "Series Y", step_stride: int = 5) -> None:
    """
    Generates a stacked layout plot of the two time-series, drawing lines 
    between paired points to visualize the temporal warping alignment.
    
    Parameters:
    -----------
    dtw_results : dict
        The output dictionary from calculate_dtw_matrices.
    x_name : str, default="Series X"
        Descriptive name of the first variable.
    y_name : str, default="Series Y"
        Descriptive name of the second variable.
    step_stride : int, default=5
        Determines how often to draw alignment lines to prevent visual clutter.
    """
    x_norm = dtw_results["x_normalized"]
    y_norm = dtw_results["y_normalized"]
    path = dtw_results["path"]
    
    plt.figure(figsize=(12, 6))
    
    # Offset the series vertically to make room for alignment lines
    plt.plot(x_norm + 2.5, label=f"{x_name} (Normalized)", color="#2b5c8f", linewidth=1.5)
    plt.plot(y_norm - 2.5, label=f"{y_name} (Normalized)", color="#d95f02", linewidth=1.5)
    
    # Draw alignment lines between matched pairs based on the stride parameter
    for idx in range(0, len(path), step_stride):
        coord_x = path[idx, 0]
        coord_y = path[idx, 1]
        plt.plot([coord_x, coord_y], [x_norm[coord_x] + 2.5, y_norm[coord_y] - 2.5], 
                 color="gray", linestyle="--", alpha=0.4, linewidth=0.8)
                 
    plt.title(f"DTW Step-by-Step Point Alignment Map ({x_name} vs {y_name})", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Sequential Data Step Indices", fontsize=11)
    plt.ylabel("Standardized Values (Offset Scale)", fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.3)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example usage with synthetically generated time-series data to verify functionality
    np.random.seed(42)
    
    # Generate a reference time-series shape (a smooth sine wave)
    time_base = np.linspace(0, 4 * np.pi, 100)
    series_alpha = np.sin(time_base) + np.random.normal(0, 0.15, 100)
    
    # Generate a second series with a shifted phase and a non-linear temporal stretch
    # (Simulating an external tracking indicator experiencing a varying propagation lag)
    warped_time_base = np.linspace(0, 4 * np.pi, 90)
    series_beta = np.sin(warped_time_base - 0.5) + np.random.normal(0, 0.15, 90)
    
    print("--- 1. Executing DTW Alignment Matrix Calculations ---")
    dtw_output = calculate_dtw_matrices(series_alpha, series_beta)
    print(f"Calculated DTW Cost Distance: {dtw_output['distance']:.5f}")
    print(f"Total alignment path coordinates captured: {len(dtw_output['path'])}")
    
    print("
--- 2. Visualizing Accumulated Cost Matrix Heatmap ---")
    plot_dtw_alignment_grid(dtw_output, x_name="Indicator Alpha", y_name="Indicator Beta")
    
    print("
--- 3. Visualizing Connected Point Mappings ---")
    plot_dtw_connected_lines(dtw_output, x_name="Indicator Alpha", y_name="Indicator Beta", step_stride=4)
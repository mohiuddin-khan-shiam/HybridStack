"""
Shapley Additive exPlanations (SHAP) Model-Agnostic Explanation Pipeline.

This module provides a standalone, production-ready framework for compressing 
background datasets via K-Means, generating local feature attributions using 
shap.KernelExplainer, and exporting high-resolution diagnostic summary graphics.
"""

import os
from typing import Callable, Union, List, Optional
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import shap


def compress_background_dataset(
    X_train: Union[pd.DataFrame, np.ndarray], 
    n_clusters: int = 50, 
    random_state: int = 42
) -> np.ndarray:
    """Compresses large training sets into representative K-Means cluster centroids.

    This compression minimizes the background data size, which drastically improves 
    the computation speed of model-agnostic conditional expectations in KernelSHAP.

    Parameters:
    -----------
    X_train : pd.DataFrame or np.ndarray
        The reference dataset used to train the predictive model.
    n_clusters : int
        The target number of cluster centroids to extract.
    random_state : int
        Deterministic seed value for reproducibility controls.

    Returns:
    --------
    centroids : np.ndarray
        Array containing the extracted cluster centers.
    """
    print(f"Compressing background dataset into {n_clusters} representative clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init="auto")
    kmeans.fit(X_train)
    return np.array(kmeans.cluster_centers_, dtype=float)


def compute_kernel_shap_values(
    prediction_function: Callable[[np.ndarray], np.ndarray],
    background_data: np.ndarray,
    X_sample: Union[pd.DataFrame, np.ndarray],
    nsamples: int = 50
) -> np.ndarray:
    """Initializes a KernelExplainer instance and computes local SHAP values.

    Parameters:
    -----------
    prediction_function : Callable[[np.ndarray], np.ndarray]
        The prediction method of the model (e.g., model.predict). Must accept 
        2D numpy arrays and return 1D or 2D numerical vectors.
    background_data : np.ndarray
        The reference data used to simulate missing feature states.
    X_sample : pd.DataFrame or np.ndarray
        The dataset instances for which feature attributions are computed.
    nsamples : int
        The number of Monte Carlo coalition samples evaluated during optimization.

    Returns:
    --------
    shap_values : np.ndarray
        Matrix containing the calculated feature attributions.
    """
    print("Initializing KernelSHAP explainer structure...")
    explainer = shap.KernelExplainer(prediction_function, background_data, nsamples=nsamples)
    
    X_sample_arr = np.array(X_sample, dtype=float)
    print(f"Computing attributions across sample population (Size: {X_sample_arr.shape[0]})...")
    shap_values = explainer.shap_values(X_sample_arr)
    
    return np.array(shap_values)


def export_high_res_summary_plot(
    shap_values: np.ndarray,
    X_sample: pd.DataFrame,
    output_dir: str = "artifacts",
    filename_prefix: str = "shap_summary",
    title: Optional[str] = None,
    width_in: float = 3.5,
    height_in: float = 4.5,
    dpi: int = 600
) -> List[str]:
    """Generates and exports a standard publication-ready SHAP dot summary plot.

    Saves the graphic in PDF (vector format), PNG, and TIFF formats.

    Parameters:
    -----------
    shap_values : np.ndarray
        The matrix of calculated SHAP feature attributions.
    X_sample : pd.DataFrame
        The feature matrix corresponding to the shap_values. A pandas DataFrame 
        is preferred to preserve feature names on the vertical axis.
    output_dir : str
        The destination directory path for the exported files.
    filename_prefix : str
        The base name used to name the exported files.
    title : str, optional
        A custom title string to display on the chart.
    width_in : float
        The targeted width dimension in inches.
    height_in : float
        The targeted height dimension in inches.
    dpi : int
        The dots-per-inch resolution quality constraint.

    Returns:
    --------
    saved_paths : List[str]
        List of absolute file paths to the exported graphics.
    """
    os.makedirs(output_dir, exist_ok=True)
    saved_paths = []

    # Configure a figure context explicitly before invoking SHAP plotting routines
    fig = plt.figure(figsize=(width_in, height_in), dpi=dpi)

    print("Generating global SHAP summary graphics context...")
    shap.summary_plot(
        shap_values,
        X_sample,
        plot_type="dot",
        color=plt.get_cmap("coolwarm"),
        show=False
    )

    if title:
        plt.title(title, pad=6)

    plt.tight_layout()

    # Define path maps
    base_path = os.path.join(output_dir, filename_prefix)
    
    # Export as lossless compressed TIFF
    tiff_path = f"{base_path}_600dpi.tif"
    plt.savefig(tiff_path, dpi=dpi, format="tiff", bbox_inches="tight",
                pil_kwargs={"compression": "tiff_lzw"})
    saved_paths.append(tiff_path)

    # Export as standard rasterized PNG
    png_path = f"{base_path}_600dpi.png"
    plt.savefig(png_path, dpi=dpi, format="png", bbox_inches="tight")
    saved_paths.append(png_path)

    # Export as scalable vector PDF
    pdf_path = f"{base_path}_600dpi.pdf"
    plt.savefig(pdf_path, format="pdf", bbox_inches="tight")
    saved_paths.append(pdf_path)

    plt.close(fig)
    print(f"Graphics successfully exported to output directory: '{output_dir}'")
    return saved_paths


if __name__ == "__main__":
    # Standalone pipeline verification using synthetic arrays
    print("Constructing synthetic environment frameworks...")
    np.random.seed(42)
    feature_labels = [f"Feature_{i}" for i in range(6)]
    
    # Generate mock data
    X_train_dummy = pd.DataFrame(np.random.randn(500, 6), columns=feature_labels)
    X_sample_dummy = pd.DataFrame(np.random.randn(20, 6), columns=feature_labels)

    # Define a mock prediction function that returns a linear combination of inputs
    def mock_predict_fn(inputs: np.ndarray) -> np.ndarray:
        return np.dot(inputs, np.array([1.5, -2.0, 0.5, 0.0, 1.1, -0.7]))

    # Step 1: Compress background data using K-Means
    bg_compressed = compress_background_dataset(X_train_dummy, n_clusters=10, random_state=42)

    # Step 2: Compute feature attributions using KernelSHAP
    calculated_shap = compute_kernel_shap_values(
        prediction_function=mock_predict_fn,
        background_data=bg_compressed,
        X_sample=X_sample_dummy,
        nsamples=30
    )

    # Step 3: Export publication-ready summary plots
    paths = export_high_res_summary_plot(
        shap_values=calculated_shap,
        X_sample=X_sample_dummy,
        output_dir="artifacts_test",
        title="SHAP Diagnostic Attributions"
    )

    print("\nPipeline execution verification completed successfully.")
    for p in paths:
        print(f"  -> File Saved: {p}")
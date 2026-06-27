"""
Principal Component Analysis (PCA) & High-Dimensional Profiling Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on multivariate datasets using PCA. It handles data validation,
standardization, eigen-decomposition, component projection, and outputs professional,
publication-grade diagnostic charts (Scree plots, score scatter plots, and loadings heatmaps)
completely independent of specific project columns or datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def run_principal_component_analysis(df: pd.DataFrame, feature_cols: list) -> dict:
    """
    Validates data, standardizes features, and executes PCA.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing multivariate numerical data.
    feature_cols : list
        List of strings containing column names to include in the analysis.
        
    Returns:
    --------
    dict
        A dictionary containing the trained PCA object, scaled data matrix, 
        transformed component scores, and formatted loadings DataFrame.
    """
    # Verify columns exist and remove rows with missing entries
    missing_cols = [col for col in feature_cols if col not in df.columns]
    if missing_cols:
        raise KeyError(f"The following features were not found in the DataFrame: {missing_cols}")
        
    clean_df = df[feature_cols].dropna().copy()
    if clean_df.empty:
        raise ValueError("The dataset is empty after filtering for the requested features and removing nulls.")
        
    # Standardize data to zero mean and unit variance
    scaler = StandardScaler()
    scaled_matrix = scaler.fit_transform(clean_df)
    
    # Fit PCA across all available components to get a complete variance overview
    pca_object = PCA()
    component_scores = pca_object.fit_transform(scaled_matrix)
    
    # Build a structured DataFrame for loading coefficients
    pc_labels = [f"PC_{i+1}" for i in range(len(feature_cols))]
    loadings_df = pd.DataFrame(
        pca_object.components_.T,
        index=feature_cols,
        columns=pc_labels
    )
    
    return {
        "pca_object": pca_object,
        "scaled_matrix": scaled_matrix,
        "scores": component_scores,
        "loadings": loadings_df,
        "features_analyzed": feature_cols
    }


def plot_scree_variance(pca_results: dict, save_path: str = None) -> None:
    """
    Generates a professional Scree plot showing both individual and cumulative 
    explained variance ratios across all components.
    
    Parameters:
    -----------
    pca_results : dict
        The output dictionary from run_principal_component_analysis.
    save_path : str, optional
        File system path where the completed plot should be saved.
    """
    pca_obj = pca_results["pca_object"]
    ind_variance = pca_obj.explained_variance_ratio_
    cum_variance = np.cumsum(ind_variance)
    num_components = len(ind_variance)
    
    fig, ax1 = plt.subplots(figsize=(10, 5))
    
    # Left Axis: Individual variance bars
    ax1.bar(range(1, num_components + 1), ind_variance, alpha=0.75, color="#2b5c8f", edgecolor="black", linewidth=0.5, label="Individual Variance")
    ax1.set_xlabel("Principal Components", fontsize=11, labelpad=8)
    ax1.set_ylabel("Individual Explained Variance Ratio", fontsize=11, color="#2b5c8f")
    ax1.tick_params(axis='y', labelcolor="#2b5c8f")
    ax1.set_xticks(range(1, num_components + 1))
    ax1.grid(True, linestyle=":", alpha=0.4)
    
    # Right Axis: Cumulative variance line
    ax2 = ax1.twinx()
    ax2.plot(range(1, num_components + 1), cum_variance, color="#e31a1c", marker="o", linewidth=2, label="Cumulative Variance")
    ax2.set_ylabel("Cumulative Explained Variance Ratio", fontsize=11, color="#e31a1c")
    ax2.tick_params(axis='y', labelcolor="#e31a1c")
    ax2.set_ylim(0, 1.05)
    
    # Add an 80% variance threshold line for reference
    ax2.axhline(0.80, color="gray", linestyle="--", linewidth=1.2, alpha=0.7)
    
    plt.title("PCA Scree Plot: Variance Decomposition Profile", fontsize=13, fontweight="bold", pad=15)
    fig.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_component_scores_2d(pca_results: dict, title: str = "PCA Component Projection Space", save_path: str = None) -> None:
    """
    Plots data samples projected onto the first two principal components.
    
    Parameters:
    -----------
    pca_results : dict
        The output dictionary from run_principal_component_analysis.
    title : str, default="PCA Component Projection Space"
        Main title for the scatter plot.
    save_path : str, optional
        File system path where the completed plot should be saved.
    """
    scores = pca_results["scores"]
    pca_obj = pca_results["pca_object"]
    
    evr_pc1 = pca_obj.explained_variance_ratio_[0] * 100
    evr_pc2 = pca_obj.explained_variance_ratio_[1] * 100
    
    plt.figure(figsize=(9, 7))
    plt.scatter(scores[:, 0], scores[:, 1], alpha=0.65, color="#2b5c8f", edgecolor="white", linewidth=0.4, s=45)
    
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    plt.axvline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.5)
    
    plt.title(title, fontsize=13, fontweight="bold", pad=15)
    plt.xlabel(f"Principal Component 1 ({evr_pc1:.1f}% Variance)", fontsize=11)
    plt.ylabel(f"Principal Component 2 ({evr_pc2:.1f}% Variance)", fontsize=11)
    
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


def plot_loadings_heatmap(pca_results: dict, max_pcs_to_show: int = 4, save_path: str = None) -> None:
    """
    Generates a color-coded heatmap of the loading weights to show 
    which original variables drive each principal component.
    
    Parameters:
    -----------
    pca_results : dict
        The output dictionary from run_principal_component_analysis.
    max_pcs_to_show : int, default=4
        The maximum number of components to display horizontally on the heatmap.
    save_path : str, optional
        File system path where the completed plot should be saved.
    """
    loadings = pca_results["loadings"]
    cols_to_render = loadings.columns[:min(max_pcs_to_show, len(loadings.columns))]
    render_df = loadings[cols_to_render]
    
    plt.figure(figsize=(8, min(8, len(render_df) * 0.6 + 2)))
    
    # Use a diverging colormap since weights swing from negative to positive
    sns.heatmap(
        render_df,
        cmap="coolwarm",
        annot=True,
        fmt=".2f",
        center=0,
        linewidths=0.5,
        cbar_kws={"label": "Loading Coefficient Weight"},
        robust=True
    )
    
    plt.title("PCA Feature Loadings Matrix", fontsize=13, fontweight="bold", pad=15)
    plt.ylabel("Original Input Features", fontsize=11)
    plt.xlabel("Extracted Principal Components", fontsize=11)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with a synthetically generated dataset to verify functionality
    np.random.seed(42)
    n_records = 150
    
    # Create an underlying unobserved driving factor to build realistic correlations
    latent_factor_1 = np.random.normal(0, 2.0, size=n_records)
    latent_factor_2 = np.random.normal(0, 1.5, size=n_records)
    
    # Construct a highly collinear multivariate dataset from the latent factors
    mock_data = pd.DataFrame({
        "Feature_A": 2.0 * latent_factor_1 + np.random.normal(0, 0.5, n_records),
        "Feature_B": -1.5 * latent_factor_1 + np.random.normal(0, 0.4, n_records),
        "Feature_C": 0.8 * latent_factor_1 + 1.2 * latent_factor_2 + np.random.normal(0, 0.3, n_records),
        "Feature_D": 3.0 * latent_factor_2 + np.random.normal(0, 0.6, n_records),
        "Feature_E": -2.2 * latent_factor_2 + np.random.normal(0, 0.5, n_records),
        "Feature_F": np.random.uniform(-5, 5, size=n_records)  # Random noise feature
    })
    
    target_cols = ["Feature_A", "Feature_B", "Feature_C", "Feature_D", "Feature_E", "Feature_F"]
    
    print("--- 1. Executing PCA Pipeline ---")
    pca_output = run_principal_component_analysis(mock_data, feature_cols=target_cols)
    print("Loadings matrix preview:")
    print(pca_output["loadings"].round(3).head())
    
    print("
--- 2. Visualizing Scree Plot ---")
    plot_scree_variance(pca_output)
    
    print("
--- 3. Visualizing 2D Component Score Projection ---")
    plot_component_scores_2d(pca_output, title="Simulated Multi-Variable Data Structure")
    
    print("
--- 4. Visualizing Component Loading Coefficients ---")
    plot_loadings_heatmap(pca_output, max_pcs_to_show=3)
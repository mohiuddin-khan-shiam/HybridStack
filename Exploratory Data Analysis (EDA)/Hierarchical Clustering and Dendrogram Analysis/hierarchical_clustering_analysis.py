"""
Hierarchical Clustering & Dendrogram Structural Profiling Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) using Agglomerative Hierarchical Clustering. It handles missing data
cleansing, automates linkage matrix calculations, computes tree validation scores 
(Cophenetic correlation), extracts actionable flat cluster assignments, and outputs 
high-quality visualization dendrograms independent of specific project datasets.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage, cophenet
from scipy.spatial.distance import pdist


def compute_hierarchical_linkage(
    data_matrix: pd.DataFrame,
    cluster_features: bool = True,
    metric: str = "euclidean",
    linkage_method: str = "ward"
) -> dict:
    """
    Validates data, computes pairwise distance structures, builds the hierarchical 
    linkage tree matrix, and calculates the Cophenetic verification score.
    
    Parameters:
    -----------
    data_matrix : pd.DataFrame
        Input DataFrame containing continuous numerical variables.
    cluster_features : bool, default=True
        If True, clusters columns (features) based on correlation profiles.
        If False, clusters rows (sample observations) directly.
    metric : str, default="euclidean"
        Distance metric for pairwise parsing ('euclidean', 'cityblock', 'cosine').
    linkage_method : str, default="ward"
        Linkage aggregation criterion ('ward', 'complete', 'average', 'single').
        Note: 'ward' requires 'euclidean' distance metric tracking.
        
    Returns:
    --------
    dict
        A dictionary containing the calculated linkage matrix, labels, cophenetic 
        correlation score, and reference configurations.
    """
    # Clean out rows with missing data values
    clean_df = data_matrix.dropna()
    
    if cluster_features:
        # Cluster features: construct a correlation matrix as the baseline space
        working_matrix = clean_df.select_dtypes(include=[np.number]).corr()
        labels = working_matrix.columns.tolist()
        # If clustering correlation, use correlation-based distance metrics
        if metric == "euclidean" and linkage_method != "ward":
            metric = "correlation"
    else:
        # Cluster sample observations directly
        working_matrix = clean_df.select_dtypes(include=[np.number])
        labels = working_matrix.index.tolist()
        
    if working_matrix.empty:
        raise ValueError("The numerical matrix is empty. Ensure columns contain continuous numbers.")
        
    if linkage_method == "ward" and metric != "euclidean":
        print("Warning: Ward linkage requires an euclidean distance metric. Forcing metric='euclidean'.")
        metric = "euclidean"
        
    # Calculate the pairwise distance vector
    pairwise_distances = pdist(working_matrix, metric=metric)
    
    # Compute the agglomerative hierarchical tree structure
    linkage_matrix = linkage(pairwise_distances, method=linkage_method)
    
    # Calculate the Cophenetic Correlation Coefficient to validate tree consistency
    coph_corr, _ = cophenet(linkage_matrix, pairwise_distances)
    
    return {
        "linkage_matrix": linkage_matrix,
        "labels": labels,
        "cophenetic_coefficient": coph_corr,
        "linkage_method": linkage_method,
        "metric": metric,
        "cluster_features": cluster_features,
        "source_data": working_matrix
    }


def extract_flat_clusters(linkage_results: dict, num_clusters: int) -> pd.Series:
    """
    Prunes the hierarchical linkage tree at a specific threshold layer to 
    extract flat, actionable group cluster IDs.
    
    Parameters:
    -----------
    linkage_results : dict
        The metric dictionary returned from compute_hierarchical_linkage.
    num_clusters : int
        The desired target number of clusters to extract from the tree.
        
    Returns:
    --------
    pd.Series
        A pandas Series mapping the node labels to their extracted cluster IDs.
    """
    linkage_matrix = linkage_results["linkage_matrix"]
    labels = linkage_results["labels"]
    
    cluster_assignments = sch.fcluster(linkage_matrix, t=num_clusters, criterion="maxclust")
    
    return pd.Series(cluster_assignments, index=labels, name="Cluster_ID")


def plot_cluster_dendrogram(
    linkage_results: dict,
    title: str = "Agglomerative Hierarchical Clustering Dendrogram",
    color_threshold: float = None,
    save_path: str = None
) -> None:
    """
    Generates a professional, publication-grade Dendrogram visualization 
    displaying branching thresholds and structural taxonomies.
    
    Parameters:
    -----------
    linkage_results : dict
        The metric dictionary returned from compute_hierarchical_linkage.
    title : str, default="Agglomerative Hierarchical Clustering Dendrogram"
        The main descriptive title for the figure.
    color_threshold : float, optional
        The distance threshold at which branches change color. 
        Leave as None to use scipy's automatic default layout.
    save_path : str, optional
        File system path where the completed plot should be saved.
    """
    linkage_matrix = linkage_results["linkage_matrix"]
    labels = linkage_results["labels"]
    coph_score = linkage_results["cophenetic_coefficient"]
    
    plt.figure(figsize=(13, 6))
    
    # Generate the dendrogram tree plot layout
    dendrogram(
        linkage_matrix,
        labels=labels,
        color_threshold=color_threshold,
        leaf_rotation=45,
        leaf_font_size=10,
        edgecolor="black",
        above_threshold_color="#555555"
    )
    
    # Configure headings and labels
    full_title = f"{title}\nMethod: {linkage_results['linkage_method']} | Cophenetic Fit Score: {coph_score:.3f}"
    plt.title(full_title, fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Features (Columns)" if linkage_results["cluster_features"] else "Observations (Rows)", fontsize=11, labelpad=10)
    plt.ylabel("Statistical Cluster Distance Threshold", fontsize=11, labelpad=10)
    
    plt.grid(axis="y", linestyle=":", alpha=0.5)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()


if __name__ == "__main__":
    # Example usage with a synthetically generated dataset to verify functionality
    np.random.seed(42)
    n_samples = 100
    
    # Generate a dataset containing blocks of highly correlated variables
    group_1 = np.random.normal(10, 2, size=(n_samples, 3))
    group_2 = np.random.normal(5, 1, size=(n_samples, 3))
    group_3 = np.random.normal(-5, 3, size=(n_samples, 2))
    
    # Combine blocks and add random noise
    mock_data_matrix = np.hstack([group_1, group_2, group_3]) + np.random.normal(0, 0.5, size=(n_samples, 8))
    
    feature_labels = [f"Indicator_{alpha}" for alpha in ["A", "B", "C", "D", "E", "F", "G", "H"]]
    mock_df = pd.DataFrame(mock_data_matrix, columns=feature_labels)
    
    print("--- 1. Computing Hierarchical Tree (Feature Mode) ---")
    clustering_output = compute_hierarchical_linkage(
        data_matrix=mock_df,
        cluster_features=True,
        linkage_method="ward"
    )
    print(f"Cophenetic Correlation Validation Score: {clustering_output['cophenetic_coefficient']:.4f}")
    
    print("
--- 2. Pruning Tree to Extract Flat Cluster Groups ---")
    # Extract 3 flat, distinct cluster groups based on the tree structure
    flat_cluster_series = extract_flat_clusters(clustering_output, num_clusters=3)
    print("Extracted Group Assignments Matrix:")
    print(flat_cluster_series)
    
    print("
--- 3. Visualizing Cluster Dendrogram ---")
    plot_cluster_dendrogram(
        linkage_results=clustering_output,
        title="Simulated Indicators Proximity Topology (Agglomerative EDA)"
    )
"""
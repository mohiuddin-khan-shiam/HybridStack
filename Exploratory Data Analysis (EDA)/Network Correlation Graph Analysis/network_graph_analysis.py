"""
Network Correlation Graph & Multivariate Topology Tool

This module provides a general-purpose, reusable framework for conducting Exploratory
Data Analysis (EDA) on high-dimensional numerical datasets using Network Graphs. It
computes complete pairwise correlation matrices, filters out statistical noise using
customizable thresholds, calculates node degree centralities, solves stable 2D spatial
positions using force-directed layout algorithms, and outputs clean, professional
network visualizations with automated label adjustments.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# Conditional check to safely handle adjustText integration
try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False


def build_correlation_network(
    df: pd.DataFrame,
    features: list,
    threshold: float = 0.65,
    correlation_type: str = "pearson"
) -> nx.Graph:
    """
    Computes a pairwise correlation matrix and builds a mathematical NetworkX graph 
    containing only the edges that exceed the specified absolute threshold.
    
    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing multivariate numerical features.
    features : list
        List of column strings to include in the network analysis.
    threshold : float, default=0.65
        The absolute correlation threshold cut-off value for adding an edge.
    correlation_type : str, default='pearson'
        The correlation metric to execute ('pearson', 'spearman', 'kendall').
        
    Returns:
    --------
    nx.Graph
        A populated NetworkX Graph object containing weighted correlation edges.
    """
    missing_features = [col for col in features if col not in df.columns]
    if missing_features:
        raise KeyError(f"The following features were not found in the DataFrame: {missing_features}")
        
    # Calculate the complete baseline correlation matrix, dropping missing rows
    corr_matrix = df[features].dropna().corr(method=correlation_type)
    
    if corr_matrix.empty:
        raise ValueError("The computed correlation matrix is empty. Verify feature data integrity.")
        
    # Instantiate the Graph object
    G = nx.Graph()
    
    # Loop through the matrix coordinates to isolate strong relationships
    columns = corr_matrix.columns
    num_cols = len(columns)
    
    for i in range(num_cols):
        for j in range(i):
            weight_val = corr_matrix.iloc[i, j]
            # Add an edge if its absolute value exceeds the threshold limit
            if abs(weight_val) > threshold:
                G.add_edge(columns[i], columns[j], weight=weight_val)
                
    # Add any remaining isolated nodes that had no connections exceeding the threshold
    for node in columns:
        if node not in G:
            G.add_node(node)
            
    return G


def plot_correlation_network(
    G: nx.Graph,
    title: str = "Network Correlation Topology Graph",
    node_color: str = "#9ecae1",
    edge_base_color: str = "gray",
    layout_k_spacing: float = 1.2,
    random_seed: int = 42,
    save_path: str = None
) -> None:
    """
    Generates a professional, publication-grade network graph visualization.
    Nodes are sized by connection degrees, and edge thicknesses scale with correlation strength.
    
    Parameters:
    -----------
    G : nx.Graph
        The populated NetworkX graph object from build_correlation_network.
    title : str, default="Network Correlation Topology Graph"
        The main descriptive title for the plot.
    node_color : str, default='#9ecae1'
        The color code used for node spheres.
    edge_base_color : str, default='gray'
        The baseline color code used for connecting lines.
    layout_k_spacing : float, default=1.2
        The optimal spacing constant parameter 'k' for the spring layout physics engine.
    random_seed : int, default=42
        Seed integer used to lock the layout generation for reproducibility.
    save_path : str, optional
        File system destination path to save the completed figure file.
    """
    if len(G.nodes) == 0:
        print("Warning: Graph contains no nodes to plot.")
        return
        
    plt.figure(figsize=(14, 12))
    
    # Calculate node sizes based on their connectivity degree
    # Isolated nodes receive a small baseline size, while connected nodes scale up
    node_sizes = [500 + (G.degree(node) * 350) for node in G.nodes()]
    
    # Extract edges and scale line thicknesses to reflect absolute correlation strengths
    edges = list(G.edges())
    if edges:
        edge_weights = [abs(G[u][v]['weight']) * 3.5 for u, v in edges]
    else:
        edge_weights = []
        
    # Solve stable 2D spatial positions using a force-directed spring layout
    pos = nx.spring_layout(G, k=layout_k_spacing, seed=random_seed)
    
    # Render edges with dynamic thicknesses
    if edges:
        nx.draw_networkx_edges(G, pos, edgelist=edges, alpha=0.4, edge_color=edge_base_color, width=edge_weights)
        
    # Render individual variable nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_color, alpha=0.85, edgecolors="black", linewidths=0.8)
    
    # Render node label texts cleanly
    texts = []
    for node, (x_coord, y_coord) in pos.items():
        texts.append(plt.text(
            x_coord, y_coord, node,
            fontsize=10, fontweight="bold",
            ha="center", va="center",
            bbox=dict(facecolor="white", alpha=0.75, edgecolor="none", boxstyle="round,pad=0.2")
        ))
        
    # Use adjustText to automatically fix label overlaps if the library is available
    if HAS_ADJUST_TEXT and texts:
        adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray", lw=0.5, alpha=0.5))
    elif not HAS_ADJUST_TEXT:
        print("Notice: install 'adjustText' to enable automatic label overlap prevention adjustments.")
        
    plt.title(title, fontsize=14, fontweight="bold", pad=20)
    plt.axis("off")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    # Example usage with synthetically generated data to verify functionality
    np.random.seed(42)
    n_samples = 120
    
    # Construct distinct blocks of correlated variables to simulate realistic economic indicators
    core_driver_1 = np.random.normal(0, 1.0, size=n_samples)
    core_driver_2 = np.random.normal(0, 1.0, size=n_samples)
    
    mock_df = pd.DataFrame({
        "Indicator_Alpha": 2.0 * core_driver_1 + np.random.normal(0, 0.4, n_samples),
        "Indicator_Beta": 1.5 * core_driver_1 + np.random.normal(0, 0.3, n_samples),
        "Indicator_Gamma": -1.8 * core_driver_1 + np.random.normal(0, 0.5, n_samples),
        "Indicator_Delta": 3.0 * core_driver_2 + np.random.normal(0, 0.4, n_samples),
        "Indicator_Epsilon": -2.5 * core_driver_2 + np.random.normal(0, 0.6, n_samples),
        "Indicator_Zeta": np.random.uniform(-3, 3, size=n_samples),  # Completely isolated feature
        "Indicator_Eta": 0.5 * core_driver_1 + 0.5 * core_driver_2 + np.random.normal(0, 0.5, n_samples) # Bridge feature
    })
    
    target_features = ["Indicator_Alpha", "Indicator_Beta", "Indicator_Gamma", "Indicator_Delta", "Indicator_Epsilon", "Indicator_Zeta", "Indicator_Eta"]
    
    print("--- 1. Generating Graph Matrix Framework ---")
    # Build graph network capturing links that exceed an absolute correlation of 0.60
    network_graph = build_correlation_network(mock_df, features=target_features, threshold=0.60, correlation_type="pearson")
    print(f"Graph constructed successfully. Total Nodes: {len(network_graph.nodes)} | Total Edges: {len(network_graph.edges)}")
    
    print("
--- 2. Launching Network Graph Visualization ---")
    plot_correlation_network(
        G=network_graph,
        title="Simulated Indicators Network Topology (Spring Layout EDA)",
        node_color="#a1d99b",
        layout_k_spacing=1.5
    )
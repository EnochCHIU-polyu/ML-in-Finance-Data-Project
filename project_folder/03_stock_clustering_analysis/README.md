# 03 Stock Clustering Analysis

## Goal
Group many stocks into behavior-based clusters for risk/return profiling and diversification.

## Folder Structure
- `data/`: Cluster outputs in CSV
- `graph/`: Clustering diagnostics and visualizations
- `implementation/`: Notebook implementation

## Data Files and Number Meaning

### cluster_feature_summary.csv
Meaning:
- Rows = cluster IDs
- Columns = average feature values for each cluster

How to read:
- Compare cluster-level average volatility, return, momentum, volume behavior

### cluster_risk_labels.csv
Meaning:
- Cluster ID mapped to risk label (Low/Medium/High)
- Risk label typically derived from cluster average volatility quantiles

How to read:
- Use as quick portfolio allocation reference

### stock_cluster_assignments.csv
Meaning:
- Each stock symbol assigned to one cluster
- Includes main feature columns used for clustering

How to read:
- Same cluster implies similar market behavior profile

## Clustering Metrics and Number Meaning
- Inertia: within-cluster sum of squares (lower better)
- Silhouette score: separation quality in [-1, 1] (higher better)
- Davies-Bouldin index: cluster overlap metric (lower better)
- PCA explained variance (%): variance captured by projected component

## Graph-by-Graph Meaning

### 01_optimal_k_selection.png
What numbers mean:
- Left panel: inertia by K
- Middle panel: silhouette by K
- Right panel: Davies-Bouldin by K

How to read:
- Choose K around elbow, high silhouette, low Davies-Bouldin jointly
- Avoid selecting K from one metric only

### 02_pca_cluster_scatter.png
What numbers mean:
- Each point = one stock
- Color = assigned cluster
- Axes = PC1/PC2 with explained variance percentages

How to read:
- Better-separated colored groups indicate clearer cluster structure
- Overlap suggests fuzzy boundaries between stock behaviors

### 03_hierarchical_dendrogram.png
What numbers mean:
- Y-axis = merge distance
- Leaves/branches represent merge sequence

How to read:
- Large vertical jumps indicate natural split levels
- Helps validate K-Means grouping reasonableness

## Practical Reporting Notes
Use these numbers in report wording:
- Final selected K rationale (multi-metric)
- Cluster behavior differences from `cluster_feature_summary.csv`
- Risk mapping from `cluster_risk_labels.csv`
- Portfolio diversification logic from assignments

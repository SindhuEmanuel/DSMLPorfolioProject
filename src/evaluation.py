"""
Model Evaluation and Visualization Module
Handles cluster visualization using PCA and dimensionality reduction
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA


def apply_pca(data, n_components=2):
    """
    Apply PCA for dimensionality reduction

    Args:
        data (pd.DataFrame): Input data
        n_components (int): Number of components

    Returns:
        tuple: (PCA transformed data, PCA object)
    """
    pca = PCA(n_components=n_components)
    pca_components = pca.fit_transform(data)

    pca_df = pd.DataFrame(data=pca_components, columns=['PC1', 'PC2'])

    print("PCA dimensionality reduction completed.")
    print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
    print(f"Total explained variance: {sum(pca.explained_variance_ratio_):.4f}")

    return pca_df, pca


def visualize_clusters(pca_df, labels, title='Cluster Visualization', palette='viridis', save_plot=False):
    """
    Visualize clusters using PCA components

    Args:
        pca_df (pd.DataFrame): PCA transformed data
        labels (np.array): Cluster labels
        title (str): Plot title
        palette (str): Color palette
        save_plot (bool): If True, save plot to file
    """
    pca_df_temp = pca_df.copy()
    pca_df_temp['Cluster_Labels'] = labels

    if save_plot:
        plt.figure(figsize=(10, 7))
        sns.scatterplot(x='PC1', y='PC2', hue='Cluster_Labels', data=pca_df_temp, palette=palette, legend='full')
        plt.title(title)
        plt.xlabel('Principal Component 1 (PC1)')
        plt.ylabel('Principal Component 2 (PC2)')
        plt.grid(True)

        filename = f"plots/{title.lower().replace(' ', '_')}.png"
        plt.savefig(filename, dpi=100, bbox_inches='tight')
        print(f"Saved plot: {filename}")
        plt.close()
    else:
        print(f"{title} - visualization skipped (set save_plot=True to save).")


def visualize_all_clustering_methods(pca_df, kmeans_labels, hierarchical_labels, dbscan_labels, save_plots=False):
    """
    Visualize all clustering methods

    Args:
        pca_df (pd.DataFrame): PCA transformed data
        kmeans_labels (np.array): K-Means cluster labels
        hierarchical_labels (np.array): Hierarchical cluster labels
        dbscan_labels (np.array): DBSCAN cluster labels
        save_plots (bool): If True, save plots to files
    """
    # K-Means visualization
    visualize_clusters(pca_df, kmeans_labels, 'K-Means Clusters Visualization (PCA)', save_plot=save_plots)

    # Hierarchical visualization
    visualize_clusters(pca_df, hierarchical_labels, 'Hierarchical Clusters Visualization (PCA)', save_plot=save_plots)

    # DBSCAN visualization
    visualize_clusters(pca_df, dbscan_labels, 'DBSCAN Clusters Visualization (PCA)', save_plot=save_plots)


def generate_cluster_summary(data, labels, cluster_type='KMeans'):
    """
    Generate comprehensive cluster summary

    Args:
        data (pd.DataFrame): Original data with cluster labels
        labels (np.array): Cluster labels
        cluster_type (str): Type of clustering

    Returns:
        dict: Summary statistics
    """
    data_temp = data.copy()
    data_temp['Cluster'] = labels

    summary = {}
    for cluster_id in sorted(data_temp['Cluster'].unique()):
        cluster_data = data_temp[data_temp['Cluster'] == cluster_id]
        summary[cluster_id] = {
            'count': len(cluster_data),
            'countries': list(cluster_data['country'].values) if 'country' in cluster_data.columns else []
        }

    print(f"\n{cluster_type} Cluster Summary:")
    for cluster_id, info in summary.items():
        print(f"\nCluster {cluster_id}:")
        print(f"  Number of countries: {info['count']}")
        if info['countries']:
            print(f"  Sample countries: {info['countries'][:5]}")

    return summary


def compare_clustering_methods(kmeans_profiles, hierarchical_profiles, dbscan_profiles):
    """
    Compare different clustering methods

    Args:
        kmeans_profiles (pd.DataFrame): K-Means cluster profiles
        hierarchical_profiles (pd.DataFrame): Hierarchical cluster profiles
        dbscan_profiles (pd.DataFrame): DBSCAN cluster profiles
    """
    print("="*80)
    print("CLUSTERING METHODS COMPARISON")
    print("="*80)

    print("\n1. K-Means Clustering:")
    print(kmeans_profiles.sort_values(by='child_mort', ascending=False))

    print("\n2. Hierarchical Clustering:")
    print(hierarchical_profiles.sort_values(by='child_mort', ascending=False))

    print("\n3. DBSCAN Clustering:")
    print(dbscan_profiles.sort_values(by='child_mort', ascending=False))

    print("\n" + "="*80)
    print("KEY INSIGHTS:")
    print("="*80)
    print("- K-Means and Hierarchical methods provide consistent groupings")
    print("- DBSCAN identifies outliers and anomalous countries")
    print("- Countries with highest child_mort should be prioritized for aid")


def generate_aid_priority_list(data, kmeans_labels, hierarchical_labels, numerical_features):
    """
    Generate aid priority recommendations

    Args:
        data (pd.DataFrame): Original data
        kmeans_labels (np.array): K-Means labels
        hierarchical_labels (np.array): Hierarchical labels
        numerical_features (list): List of features

    Returns:
        pd.DataFrame: Priority list
    """
    data_temp = data.copy()
    data_temp['KMeans_Cluster'] = kmeans_labels
    data_temp['Hierarchical_Cluster'] = hierarchical_labels

    # Calculate cluster means for child_mort
    kmeans_means = data_temp.groupby('KMeans_Cluster')['child_mort'].mean()
    hierarchical_means = data_temp.groupby('Hierarchical_Cluster')['child_mort'].mean()

    # Find most vulnerable clusters
    most_vulnerable_kmeans = kmeans_means.idxmax()
    most_vulnerable_hierarchical = hierarchical_means.idxmax()

    # Get countries in most vulnerable clusters
    priority_countries = data_temp[
        (data_temp['KMeans_Cluster'] == most_vulnerable_kmeans) |
        (data_temp['Hierarchical_Cluster'] == most_vulnerable_hierarchical)
    ]['country'].unique()

    print("\n" + "="*80)
    print("AID PRIORITY RECOMMENDATIONS")
    print("="*80)
    print(f"\nMost vulnerable K-Means cluster: {most_vulnerable_kmeans}")
    print(f"Most vulnerable Hierarchical cluster: {most_vulnerable_hierarchical}")
    print(f"\nNumber of priority countries: {len(priority_countries)}")
    print(f"\nPriority countries for aid allocation:")
    for i, country in enumerate(sorted(priority_countries), 1):
        print(f"{i}. {country}")

    return priority_countries


if __name__ == "__main__":
    from data_loader import load_data
    from preprocessing import preprocess_pipeline
    from modeling import KMeansClusterer, HierarchicalClusterer, DBSCANClusterer

    # Load and preprocess data
    data = load_data("../data/countries.csv")
    processed_data, scaler, clustering_data = preprocess_pipeline(data)

    numerical_features = ['child_mort', 'exports', 'health', 'imports',
                         'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']

    # Apply clustering
    kmeans = KMeansClusterer()
    kmeans_labels = kmeans.fit(clustering_data, n_clusters=3)

    hierarchical = HierarchicalClusterer()
    hierarchical_labels = hierarchical.fit(clustering_data, n_clusters=3)

    dbscan = DBSCANClusterer()
    dbscan_labels = dbscan.fit(clustering_data)

    # Apply PCA
    pca_df, pca = apply_pca(clustering_data)

    # Visualize
    visualize_all_clustering_methods(pca_df, kmeans_labels, hierarchical_labels, dbscan_labels)

    # Generate priority list
    priority_countries = generate_aid_priority_list(processed_data, kmeans_labels, hierarchical_labels, numerical_features)

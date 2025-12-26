"""
Clustering Models Module
Implements K-Means, Hierarchical, and DBSCAN clustering
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage, dendrogram
import joblib


class KMeansClusterer:
    """K-Means clustering implementation"""

    def __init__(self, max_clusters=10):
        """
        Initialize K-Means clusterer

        Args:
            max_clusters (int): Maximum number of clusters to test
        """
        self.max_clusters = max_clusters
        self.model = None
        self.optimal_k = None
        self.wcss = []
        self.silhouette_scores = []

    def find_optimal_k(self, data):
        """
        Find optimal number of clusters using Elbow and Silhouette methods

        Args:
            data (pd.DataFrame): Input data

        Returns:
            int: Optimal number of clusters
        """
        # Elbow method
        self.wcss = []
        for i in range(1, self.max_clusters + 1):
            kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, n_init=10)
            kmeans.fit(data)
            self.wcss.append(kmeans.inertia_)

        print("WCSS (inertia) values calculated for k from 1 to", self.max_clusters)

        # Silhouette score
        self.silhouette_scores = []
        for i in range(2, self.max_clusters + 1):
            kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, n_init=10)
            kmeans.fit(data)
            labels = kmeans.labels_
            sil_score = silhouette_score(data, labels)
            self.silhouette_scores.append(sil_score)

        print("Silhouette scores calculated for k from 2 to", self.max_clusters)

    def plot_elbow(self, save_plot=False):
        """Plot elbow curve"""
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, self.max_clusters + 1), self.wcss, marker='o', linestyle='--')
        plt.title('Elbow Method For Optimal k')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('WCSS (Within-Cluster Sum of Squares)')
        plt.xticks(range(1, self.max_clusters + 1))
        plt.grid(True)

        if save_plot:
            plt.savefig('plots/kmeans_elbow.png', dpi=100, bbox_inches='tight')
            print("Saved plot: plots/kmeans_elbow.png")

        plt.close()

    def plot_silhouette(self, save_plot=False):
        """Plot silhouette scores"""
        plt.figure(figsize=(10, 6))
        plt.plot(range(2, self.max_clusters + 1), self.silhouette_scores, marker='o', linestyle='--')
        plt.title('Silhouette Score For Optimal k')
        plt.xlabel('Number of clusters (k)')
        plt.ylabel('Silhouette Score')
        plt.xticks(range(2, self.max_clusters + 1))
        plt.grid(True)

        if save_plot:
            plt.savefig('plots/kmeans_silhouette.png', dpi=100, bbox_inches='tight')
            print("Saved plot: plots/kmeans_silhouette.png")

        plt.close()

    def fit(self, data, n_clusters=3):
        """
        Fit K-Means model

        Args:
            data (pd.DataFrame): Input data
            n_clusters (int): Number of clusters

        Returns:
            np.array: Cluster labels
        """
        self.optimal_k = n_clusters
        self.model = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=10)
        labels = self.model.fit_predict(data)

        print(f"K-Means model trained with k={n_clusters} clusters.")
        return labels

    def save_model(self, filepath):
        """Save trained model"""
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")


class HierarchicalClusterer:
    """Hierarchical clustering implementation"""

    def __init__(self):
        """Initialize Hierarchical clusterer"""
        self.model = None
        self.linkage_matrix = None

    def compute_linkage(self, data, method='ward', metric='euclidean'):
        """
        Compute linkage matrix

        Args:
            data (pd.DataFrame): Input data
            method (str): Linkage method
            metric (str): Distance metric

        Returns:
            np.array: Linkage matrix
        """
        self.linkage_matrix = linkage(data, method=method, metric=metric)
        return self.linkage_matrix

    def plot_dendrogram(self, save_plot=False):
        """Plot dendrogram"""
        if save_plot:
            plt.figure(figsize=(20, 10))
            dendrogram(self.linkage_matrix,
                      orientation='top',
                      distance_sort='descending',
                      show_leaf_counts=True)
            plt.title('Dendrogram for Hierarchical Clustering')
            plt.xlabel('Country Index')
            plt.ylabel('Distance')
            plt.savefig('plots/hierarchical_dendrogram.png', dpi=100, bbox_inches='tight')
            print("Saved plot: plots/hierarchical_dendrogram.png")
            plt.close()
        else:
            print("Dendrogram computed (set save_plot=True to save).")

    def fit(self, data, n_clusters=3):
        """
        Fit Hierarchical clustering model

        Args:
            data (pd.DataFrame): Input data
            n_clusters (int): Number of clusters

        Returns:
            np.array: Cluster labels
        """
        self.model = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
        labels = self.model.fit_predict(data)

        print(f"Hierarchical Clustering model trained with k={n_clusters} clusters.")
        return labels


class DBSCANClusterer:
    """DBSCAN clustering implementation"""

    def __init__(self, eps=1.5, min_samples=3):
        """
        Initialize DBSCAN clusterer

        Args:
            eps (float): Maximum distance between samples
            min_samples (int): Minimum samples in neighborhood
        """
        self.eps = eps
        self.min_samples = min_samples
        self.model = None

    def fit(self, data):
        """
        Fit DBSCAN model

        Args:
            data (pd.DataFrame): Input data

        Returns:
            np.array: Cluster labels
        """
        self.model = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        labels = self.model.fit_predict(data)

        unique_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        noise_points = list(labels).count(-1)

        print(f"Number of unique DBSCAN clusters found: {unique_clusters}")
        print(f"Number of noise points (outliers) detected: {noise_points}")

        return labels


def analyze_cluster_profiles(data, labels, numerical_features, cluster_type='KMeans'):
    """
    Analyze and display cluster profiles

    Args:
        data (pd.DataFrame): Original data
        labels (np.array): Cluster labels
        numerical_features (list): List of numerical features
        cluster_type (str): Type of clustering method

    Returns:
        pd.DataFrame: Cluster profiles
    """
    data_temp = data.copy()
    data_temp[f'{cluster_type}_Cluster_Labels'] = labels

    cluster_profiles = data_temp.groupby(f'{cluster_type}_Cluster_Labels')[numerical_features].mean()

    print(f"\n{cluster_type} Cluster Profiles (Mean values of features per cluster):")
    print(cluster_profiles)

    print(f"\nSorted by 'child_mort' (descending) to highlight vulnerable clusters:")
    print(cluster_profiles.sort_values(by='child_mort', ascending=False))

    return cluster_profiles


if __name__ == "__main__":
    from data_loader import load_data
    from preprocessing import preprocess_pipeline

    # Load and preprocess data
    data = load_data("../data/countries.csv")
    processed_data, scaler, clustering_data = preprocess_pipeline(data)

    # K-Means
    kmeans = KMeansClusterer(max_clusters=10)
    kmeans.find_optimal_k(clustering_data)
    kmeans.plot_elbow()
    kmeans.plot_silhouette()
    kmeans_labels = kmeans.fit(clustering_data, n_clusters=3)

    # Hierarchical
    hierarchical = HierarchicalClusterer()
    hierarchical.compute_linkage(clustering_data)
    hierarchical.plot_dendrogram()
    hierarchical_labels = hierarchical.fit(clustering_data, n_clusters=3)

    # DBSCAN
    dbscan = DBSCANClusterer(eps=1.5, min_samples=3)
    dbscan_labels = dbscan.fit(clustering_data)

"""
Main script to run the complete analysis pipeline
Execute this script to run the full analysis from start to finish
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import load_data, print_data_info
from eda import perform_full_eda
from stats import perform_all_hypothesis_tests
from preprocessing import preprocess_pipeline
from modeling import KMeansClusterer, HierarchicalClusterer, DBSCANClusterer, analyze_cluster_profiles
from evaluation import apply_pca, visualize_all_clustering_methods, generate_aid_priority_list


def main():
    """Run complete analysis pipeline"""

    print("="*80)
    print("COUNTRY AID CLUSTERING - COMPLETE ANALYSIS PIPELINE")
    print("="*80)

    # 1. Load Data
    print("\n[STEP 1/7] Loading data...")
    data = load_data("data/countries.csv")
    print_data_info(data)

    # 2. Exploratory Data Analysis
    print("\n[STEP 2/7] Performing EDA...")
    data = perform_full_eda(data)

    # 3. Statistical Analysis
    print("\n[STEP 3/7] Performing hypothesis tests...")
    stats_results = perform_all_hypothesis_tests(data)

    # 4. Preprocessing
    print("\n[STEP 4/7] Preprocessing data...")
    processed_data, scaler, clustering_data = preprocess_pipeline(data)

    # Define features
    numerical_features = ['child_mort', 'exports', 'health', 'imports',
                         'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']

    # 5. Clustering
    print("\n[STEP 5/7] Training clustering models...")

    # K-Means
    print("\n--- K-Means Clustering ---")
    kmeans = KMeansClusterer(max_clusters=10)
    kmeans.find_optimal_k(clustering_data)
    kmeans.plot_elbow()
    kmeans.plot_silhouette()
    kmeans_labels = kmeans.fit(clustering_data, n_clusters=3)
    kmeans_profiles = analyze_cluster_profiles(processed_data, kmeans_labels, numerical_features, 'KMeans')

    # Save K-Means model
    os.makedirs('models', exist_ok=True)
    kmeans.save_model('models/kmeans_model.pkl')

    # Hierarchical
    print("\n--- Hierarchical Clustering ---")
    hierarchical = HierarchicalClusterer()
    hierarchical.compute_linkage(clustering_data)
    hierarchical.plot_dendrogram()
    hierarchical_labels = hierarchical.fit(clustering_data, n_clusters=3)
    hierarchical_profiles = analyze_cluster_profiles(processed_data, hierarchical_labels,
                                                     numerical_features, 'Hierarchical')

    # DBSCAN
    print("\n--- DBSCAN Clustering ---")
    dbscan = DBSCANClusterer(eps=1.5, min_samples=3)
    dbscan_labels = dbscan.fit(clustering_data)
    dbscan_profiles = analyze_cluster_profiles(processed_data, dbscan_labels, numerical_features, 'DBSCAN')

    # 6. Evaluation
    print("\n[STEP 6/7] Evaluating and visualizing results...")
    pca_df, pca = apply_pca(clustering_data)
    visualize_all_clustering_methods(pca_df, kmeans_labels, hierarchical_labels, dbscan_labels)

    # 7. Generate Priority List
    print("\n[STEP 7/7] Generating aid priority recommendations...")
    priority_countries = generate_aid_priority_list(processed_data, kmeans_labels,
                                                    hierarchical_labels, numerical_features)

    # Save results
    print("\nSaving results...")
    results_data = data.copy()
    results_data['KMeans_Cluster'] = kmeans_labels
    results_data['Hierarchical_Cluster'] = hierarchical_labels
    results_data['DBSCAN_Cluster'] = dbscan_labels

    results_data.to_csv('data/clustering_results.csv', index=False)
    print("Results saved to 'data/clustering_results.csv'")

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nNext steps:")
    print("1. Review the generated visualizations")
    print("2. Examine the clustering results in 'data/clustering_results.csv'")
    print("3. Launch the Streamlit app: cd deployment && streamlit run app.py")
    print("4. Launch the Flask API: cd deployment && python api.py")


if __name__ == "__main__":
    main()

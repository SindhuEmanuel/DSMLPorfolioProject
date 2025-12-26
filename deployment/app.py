"""
Streamlit Web Application for Country Aid Clustering
Provides interactive UI for stakeholders to explore clustering results
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, src_dir)

from data_loader import load_data
from preprocessing import preprocess_pipeline
from modeling import KMeansClusterer, HierarchicalClusterer, DBSCANClusterer, analyze_cluster_profiles
from evaluation import apply_pca, visualize_clusters
import joblib

# Set matplotlib backend for deployment
import matplotlib
matplotlib.use('Agg')


# Page configuration
st.set_page_config(
    page_title="HELP International - Country Aid Clustering",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #ff7f0e;
        margin-top: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_and_process_data():
    """Load and preprocess data (cached)"""
    # Handle both local and deployment paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_path = os.path.join(parent_dir, 'data', 'countries.csv')

    # If data doesn't exist, try to download it
    if not os.path.exists(data_path):
        st.info("Downloading country data...")
        import gdown
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        file_id = '1IRQWbO9m-c93XjDsbtt2nqv5RVldVPzj'
        url = f'https://drive.google.com/uc?id={file_id}'
        gdown.download(url, data_path, quiet=False)

    data = load_data(data_path)
    processed_data, scaler, clustering_data = preprocess_pipeline(data)
    return data, processed_data, scaler, clustering_data


@st.cache_resource
def train_models(clustering_data):
    """Train all clustering models (cached)"""
    numerical_features = ['child_mort', 'exports', 'health', 'imports',
                         'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']

    # K-Means
    kmeans = KMeansClusterer()
    kmeans_labels = kmeans.fit(clustering_data, n_clusters=3)

    # Hierarchical
    hierarchical = HierarchicalClusterer()
    hierarchical_labels = hierarchical.fit(clustering_data, n_clusters=3)

    # DBSCAN
    dbscan = DBSCANClusterer(eps=1.5, min_samples=3)
    dbscan_labels = dbscan.fit(clustering_data)

    # PCA
    pca_df, pca = apply_pca(clustering_data)

    return {
        'kmeans': kmeans,
        'kmeans_labels': kmeans_labels,
        'hierarchical': hierarchical,
        'hierarchical_labels': hierarchical_labels,
        'dbscan': dbscan,
        'dbscan_labels': dbscan_labels,
        'pca_df': pca_df,
        'pca': pca
    }


def main():
    """Main Streamlit application"""

    # Header
    st.markdown('<p class="main-header">🌍 HELP International - Strategic Aid Allocation Dashboard</p>',
                unsafe_allow_html=True)

    st.markdown("""
    This dashboard helps HELP International identify countries most in need of aid using machine learning clustering techniques.
    Explore different clustering methods and their insights to make data-driven decisions for aid allocation.
    """)

    # Load data
    with st.spinner("Loading data..."):
        data, processed_data, scaler, clustering_data = load_and_process_data()

    # Train models
    with st.spinner("Training clustering models..."):
        models = train_models(clustering_data)

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Overview", "Data Exploration", "Clustering Analysis", "Aid Priority List", "Country Prediction"]
    )

    numerical_features = ['child_mort', 'exports', 'health', 'imports',
                         'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']

    if page == "Overview":
        show_overview(data, processed_data)

    elif page == "Data Exploration":
        show_data_exploration(data, processed_data)

    elif page == "Clustering Analysis":
        show_clustering_analysis(processed_data, models, numerical_features)

    elif page == "Aid Priority List":
        show_priority_list(data, processed_data, models, numerical_features)

    elif page == "Country Prediction":
        show_country_prediction(data, scaler, models)


def show_overview(data, processed_data):
    """Display overview page"""
    st.markdown('<p class="sub-header">📊 Dataset Overview</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Countries", len(data))

    with col2:
        st.metric("Features", len(data.columns) - 1)

    with col3:
        st.metric("Missing Values", data.isnull().sum().sum())

    with col4:
        avg_child_mort = data['child_mort'].mean()
        st.metric("Avg Child Mortality", f"{avg_child_mort:.2f}")

    st.markdown("---")

    st.subheader("Sample Data")
    st.dataframe(data.head(10))

    st.subheader("Statistical Summary")
    st.dataframe(data.describe())


def show_data_exploration(data, processed_data):
    """Display data exploration page"""
    st.markdown('<p class="sub-header">🔍 Data Exploration</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Distributions", "Correlations", "Country Search"])

    with tab1:
        st.subheader("Feature Distributions")
        feature = st.selectbox("Select Feature", ['child_mort', 'income', 'gdpp', 'life_expec', 'health'])

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Histogram
        ax1.hist(data[feature], bins=30, edgecolor='black')
        ax1.set_title(f'Distribution of {feature}')
        ax1.set_xlabel(feature)
        ax1.set_ylabel('Frequency')

        # Box plot
        ax2.boxplot(data[feature])
        ax2.set_title(f'Box Plot of {feature}')
        ax2.set_ylabel(feature)

        st.pyplot(fig)

    with tab2:
        st.subheader("Correlation Matrix")
        numerical_cols = data.select_dtypes(include=np.number).columns
        corr_matrix = data[numerical_cols].corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        st.pyplot(fig)

    with tab3:
        st.subheader("Search Country Data")
        country = st.selectbox("Select Country", sorted(data['country'].unique()))

        if country:
            country_data = data[data['country'] == country].iloc[0]
            st.write("### Country Statistics")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Child Mortality", f"{country_data['child_mort']:.2f}")
                st.metric("Income", f"${country_data['income']:.2f}")
                st.metric("GDP per Capita", f"${country_data['gdpp']:.2f}")
                st.metric("Life Expectancy", f"{country_data['life_expec']:.2f}")

            with col2:
                st.metric("Health Spending", f"{country_data['health']:.2f}%")
                st.metric("Exports", f"{country_data['exports']:.2f}%")
                st.metric("Imports", f"{country_data['imports']:.2f}%")
                st.metric("Inflation", f"{country_data['inflation']:.2f}%")


def show_clustering_analysis(processed_data, models, numerical_features):
    """Display clustering analysis page"""
    st.markdown('<p class="sub-header">🎯 Clustering Analysis</p>', unsafe_allow_html=True)

    method = st.selectbox("Select Clustering Method", ["K-Means", "Hierarchical", "DBSCAN"])

    if method == "K-Means":
        labels = models['kmeans_labels']
        st.write("### K-Means Clustering Results")
        st.write(f"**Number of Clusters:** 3")

    elif method == "Hierarchical":
        labels = models['hierarchical_labels']
        st.write("### Hierarchical Clustering Results")
        st.write(f"**Number of Clusters:** 3")

    else:
        labels = models['dbscan_labels']
        unique_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        noise_points = list(labels).count(-1)
        st.write("### DBSCAN Clustering Results")
        st.write(f"**Number of Clusters:** {unique_clusters}")
        st.write(f"**Noise Points (Outliers):** {noise_points}")

    # Cluster visualization
    st.subheader("Cluster Visualization (PCA)")
    pca_df = models['pca_df'].copy()
    pca_df['Cluster'] = labels

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(pca_df['PC1'], pca_df['PC2'], c=pca_df['Cluster'], cmap='viridis', s=100, alpha=0.6)
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_title(f'{method} Clusters (PCA Projection)')
    plt.colorbar(scatter, ax=ax, label='Cluster')
    st.pyplot(fig)

    # Cluster profiles
    st.subheader("Cluster Profiles")
    temp_data = processed_data.copy()
    temp_data['Cluster'] = labels
    cluster_profiles = temp_data.groupby('Cluster')[numerical_features].mean()

    st.dataframe(cluster_profiles.style.background_gradient(cmap='RdYlGn_r', subset=['child_mort']))

    # Cluster sizes
    st.subheader("Cluster Sizes")
    cluster_sizes = pd.Series(labels).value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    cluster_sizes.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_xlabel('Cluster')
    ax.set_ylabel('Number of Countries')
    ax.set_title('Countries per Cluster')
    st.pyplot(fig)


def show_priority_list(data, processed_data, models, numerical_features):
    """Display aid priority list"""
    st.markdown('<p class="sub-header">🎯 Aid Priority Recommendations</p>', unsafe_allow_html=True)

    # Combine K-Means and Hierarchical results
    temp_data = data.copy()
    temp_data['KMeans_Cluster'] = models['kmeans_labels']
    temp_data['Hierarchical_Cluster'] = models['hierarchical_labels']

    # Find most vulnerable clusters
    processed_temp = processed_data.copy()
    processed_temp['KMeans_Cluster'] = models['kmeans_labels']
    kmeans_means = processed_temp.groupby('KMeans_Cluster')['child_mort'].mean()
    most_vulnerable_cluster = kmeans_means.idxmax()

    # Get priority countries
    priority_data = temp_data[temp_data['KMeans_Cluster'] == most_vulnerable_cluster].copy()
    priority_data = priority_data.sort_values('child_mort', ascending=False)

    st.write(f"### High Priority Countries (Cluster {most_vulnerable_cluster})")
    st.write(f"**Total Countries:** {len(priority_data)}")

    # Display priority countries
    display_cols = ['country', 'child_mort', 'income', 'gdpp', 'life_expec', 'health']
    st.dataframe(
        priority_data[display_cols].style.background_gradient(cmap='RdYlGn_r', subset=['child_mort'])
    )

    # Download button
    csv = priority_data[display_cols].to_csv(index=False)
    st.download_button(
        label="Download Priority List (CSV)",
        data=csv,
        file_name="priority_countries.csv",
        mime="text/csv"
    )


def show_country_prediction(data, scaler, models):
    """Display country prediction page"""
    st.markdown('<p class="sub-header">🔮 Predict Country Cluster</p>', unsafe_allow_html=True)

    st.write("Enter country data to predict which cluster it belongs to:")

    col1, col2 = st.columns(2)

    with col1:
        child_mort = st.number_input("Child Mortality Rate", min_value=0.0, value=20.0)
        exports = st.number_input("Exports (% of GDP)", min_value=0.0, value=30.0)
        health = st.number_input("Health Spending (% of GDP)", min_value=0.0, value=6.0)
        imports = st.number_input("Imports (% of GDP)", min_value=0.0, value=35.0)
        income = st.number_input("Income per Person", min_value=0.0, value=10000.0)

    with col2:
        inflation = st.number_input("Inflation Rate (%)", min_value=-20.0, value=5.0)
        life_expec = st.number_input("Life Expectancy", min_value=0.0, value=70.0)
        total_fer = st.number_input("Total Fertility Rate", min_value=0.0, value=2.5)
        gdpp = st.number_input("GDP per Capita", min_value=0.0, value=8000.0)

    if st.button("Predict Cluster"):
        # Create input array
        input_data = np.array([[child_mort, exports, health, imports, income,
                               inflation, life_expec, total_fer, gdpp]])

        # Standardize
        input_scaled = scaler.transform(input_data)

        # Predict
        kmeans_pred = models['kmeans'].model.predict(input_scaled)[0]

        st.success(f"### Predicted Cluster: {kmeans_pred}")

        # Show cluster characteristics
        processed_temp = pd.DataFrame()
        processed_temp['child_mort'] = data['child_mort']
        processed_temp['Cluster'] = models['kmeans_labels']
        cluster_profile = processed_temp.groupby('Cluster')['child_mort'].mean()

        st.write("### Cluster Characteristics")
        st.write(f"Average child mortality in cluster {kmeans_pred}: {cluster_profile[kmeans_pred]:.2f}")

        if kmeans_pred == cluster_profile.idxmax():
            st.warning("⚠️ This country falls into the HIGH PRIORITY cluster for aid allocation.")
        else:
            st.info("ℹ️ This country is in a moderate or low priority cluster.")


if __name__ == "__main__":
    main()

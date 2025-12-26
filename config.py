"""
Configuration file for Country Aid Clustering Project
Centralized configuration management
"""

import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATA_FILE = os.path.join(DATA_DIR, 'countries.csv')

# Model paths
MODEL_DIR = os.path.join(BASE_DIR, 'models')
KMEANS_MODEL_PATH = os.path.join(MODEL_DIR, 'kmeans_model.pkl')
HIERARCHICAL_MODEL_PATH = os.path.join(MODEL_DIR, 'hierarchical_model.pkl')
DBSCAN_MODEL_PATH = os.path.join(MODEL_DIR, 'dbscan_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

# Feature configuration
NUMERICAL_FEATURES = [
    'child_mort',
    'exports',
    'health',
    'imports',
    'income',
    'inflation',
    'life_expec',
    'total_fer',
    'gdpp'
]

# Clustering configuration
CLUSTERING_CONFIG = {
    'kmeans': {
        'n_clusters': 3,
        'init': 'k-means++',
        'random_state': 42,
        'n_init': 10,
        'max_iter': 300
    },
    'hierarchical': {
        'n_clusters': 3,
        'linkage': 'ward',
        'metric': 'euclidean'
    },
    'dbscan': {
        'eps': 1.5,
        'min_samples': 3,
        'metric': 'euclidean'
    }
}

# Outlier handling configuration
OUTLIER_COLUMNS = ['child_mort', 'income', 'gdpp']
OUTLIER_METHOD = 'winsorization'  # or 'removal'
IQR_MULTIPLIER = 1.5

# Visualization configuration
VIZ_CONFIG = {
    'figure_size': (12, 8),
    'color_palette': 'viridis',
    'dpi': 100,
    'save_plots': False,
    'plot_dir': os.path.join(BASE_DIR, 'plots')
}

# API configuration
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# Streamlit configuration
STREAMLIT_CONFIG = {
    'page_title': 'HELP International - Country Aid Clustering',
    'page_icon': '🌍',
    'layout': 'wide'
}

# Statistical testing configuration
STATS_CONFIG = {
    'significance_level': 0.05,
    'test_type': 'two-sided'
}

# PCA configuration
PCA_CONFIG = {
    'n_components': 2,
    'random_state': 42
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': os.path.join(BASE_DIR, 'logs', 'app.log')
}

# Create necessary directories
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(VIZ_CONFIG['plot_dir'], exist_ok=True)
os.makedirs(os.path.dirname(LOGGING_CONFIG['log_file']), exist_ok=True)


def get_config():
    """
    Get complete configuration dictionary

    Returns:
        dict: Complete configuration
    """
    return {
        'base_dir': BASE_DIR,
        'data': {
            'dir': DATA_DIR,
            'file': DATA_FILE
        },
        'models': {
            'dir': MODEL_DIR,
            'kmeans': KMEANS_MODEL_PATH,
            'hierarchical': HIERARCHICAL_MODEL_PATH,
            'dbscan': DBSCAN_MODEL_PATH,
            'scaler': SCALER_PATH
        },
        'features': NUMERICAL_FEATURES,
        'clustering': CLUSTERING_CONFIG,
        'outliers': {
            'columns': OUTLIER_COLUMNS,
            'method': OUTLIER_METHOD,
            'iqr_multiplier': IQR_MULTIPLIER
        },
        'visualization': VIZ_CONFIG,
        'api': API_CONFIG,
        'streamlit': STREAMLIT_CONFIG,
        'statistics': STATS_CONFIG,
        'pca': PCA_CONFIG,
        'logging': LOGGING_CONFIG
    }


if __name__ == '__main__':
    import pprint
    config = get_config()
    print("Current Configuration:")
    pprint.pprint(config)

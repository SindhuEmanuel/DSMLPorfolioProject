"""
Flask REST API for Country Aid Clustering
Provides programmatic access to clustering predictions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
import sys
import os
import joblib

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import load_data
from preprocessing import preprocess_pipeline
from modeling import KMeansClusterer

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Global variables for model and scaler
MODEL = None
SCALER = None
DATA = None
CLUSTER_PROFILES = None


def initialize_model():
    """Initialize and train the model"""
    global MODEL, SCALER, DATA, CLUSTER_PROFILES

    print("Initializing model...")

    # Load data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'countries.csv')
    DATA = load_data(data_path)

    # Preprocess
    processed_data, scaler, clustering_data = preprocess_pipeline(DATA)
    SCALER = scaler

    # Train K-Means model
    kmeans = KMeansClusterer()
    labels = kmeans.fit(clustering_data, n_clusters=3)

    MODEL = kmeans.model

    # Calculate cluster profiles
    numerical_features = ['child_mort', 'exports', 'health', 'imports',
                         'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']

    temp_data = processed_data.copy()
    temp_data['Cluster'] = labels
    CLUSTER_PROFILES = temp_data.groupby('Cluster')[numerical_features].mean().to_dict('index')

    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'kmeans_model.pkl')
    scaler_path = os.path.join(model_dir, 'scaler.pkl')

    joblib.dump(MODEL, model_path)
    joblib.dump(SCALER, scaler_path)

    print("Model initialized and saved successfully!")


@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'HELP International - Country Aid Clustering API',
        'version': '1.0',
        'endpoints': {
            '/predict': 'POST - Predict cluster for country data',
            '/clusters': 'GET - Get cluster profiles',
            '/countries': 'GET - Get all countries and their clusters',
            '/priority': 'GET - Get priority countries for aid'
        }
    })


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict cluster for given country data

    Expected JSON format:
    {
        "child_mort": 20.0,
        "exports": 30.0,
        "health": 6.0,
        "imports": 35.0,
        "income": 10000.0,
        "inflation": 5.0,
        "life_expec": 70.0,
        "total_fer": 2.5,
        "gdpp": 8000.0
    }
    """
    try:
        # Get JSON data
        data = request.get_json()

        # Validate required fields
        required_fields = ['child_mort', 'exports', 'health', 'imports', 'income',
                          'inflation', 'life_expec', 'total_fer', 'gdpp']

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create input array
        input_data = np.array([[
            data['child_mort'],
            data['exports'],
            data['health'],
            data['imports'],
            data['income'],
            data['inflation'],
            data['life_expec'],
            data['total_fer'],
            data['gdpp']
        ]])

        # Standardize
        input_scaled = SCALER.transform(input_data)

        # Predict
        cluster = int(MODEL.predict(input_scaled)[0])

        # Get cluster profile
        cluster_profile = CLUSTER_PROFILES.get(cluster, {})

        # Determine priority level
        priority = determine_priority(cluster, cluster_profile)

        return jsonify({
            'cluster': cluster,
            'priority_level': priority,
            'cluster_profile': cluster_profile,
            'recommendation': get_recommendation(cluster, priority)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clusters', methods=['GET'])
def get_clusters():
    """Get all cluster profiles"""
    try:
        return jsonify({
            'clusters': CLUSTER_PROFILES,
            'num_clusters': len(CLUSTER_PROFILES)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/countries', methods=['GET'])
def get_countries():
    """Get all countries with their cluster assignments"""
    try:
        # Reload and process data
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'countries.csv')
        data = load_data(data_path)
        processed_data, _, clustering_data = preprocess_pipeline(data)

        # Predict clusters
        labels = MODEL.predict(SCALER.transform(clustering_data))

        # Create response
        result = []
        for idx, row in data.iterrows():
            result.append({
                'country': row['country'],
                'cluster': int(labels[idx]),
                'child_mort': float(row['child_mort']),
                'income': float(row['income']),
                'gdpp': float(row['gdpp']),
                'life_expec': float(row['life_expec'])
            })

        return jsonify({
            'countries': result,
            'total_countries': len(result)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/priority', methods=['GET'])
def get_priority_countries():
    """Get priority countries for aid allocation"""
    try:
        # Find most vulnerable cluster (highest avg child_mort)
        max_child_mort = -float('inf')
        vulnerable_cluster = 0

        for cluster_id, profile in CLUSTER_PROFILES.items():
            if profile['child_mort'] > max_child_mort:
                max_child_mort = profile['child_mort']
                vulnerable_cluster = cluster_id

        # Get countries in vulnerable cluster
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'countries.csv')
        data = load_data(data_path)
        processed_data, _, clustering_data = preprocess_pipeline(data)

        labels = MODEL.predict(SCALER.transform(clustering_data))

        priority_countries = []
        for idx, row in data.iterrows():
            if labels[idx] == vulnerable_cluster:
                priority_countries.append({
                    'country': row['country'],
                    'child_mort': float(row['child_mort']),
                    'income': float(row['income']),
                    'gdpp': float(row['gdpp']),
                    'life_expec': float(row['life_expec']),
                    'health': float(row['health'])
                })

        # Sort by child mortality (descending)
        priority_countries.sort(key=lambda x: x['child_mort'], reverse=True)

        return jsonify({
            'vulnerable_cluster': int(vulnerable_cluster),
            'priority_countries': priority_countries,
            'total_priority_countries': len(priority_countries),
            'cluster_profile': CLUSTER_PROFILES[vulnerable_cluster]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def determine_priority(cluster, cluster_profile):
    """Determine priority level based on cluster characteristics"""
    child_mort = cluster_profile.get('child_mort', 0)

    # Thresholds (based on standardized values)
    if child_mort > 0.5:
        return 'HIGH'
    elif child_mort > -0.5:
        return 'MEDIUM'
    else:
        return 'LOW'


def get_recommendation(cluster, priority):
    """Get aid recommendation based on cluster and priority"""
    recommendations = {
        'HIGH': 'Urgent aid required. Focus on healthcare infrastructure, poverty reduction, and basic needs.',
        'MEDIUM': 'Moderate aid required. Focus on sustainable development and capacity building.',
        'LOW': 'Minimal aid required. Country shows good development indicators.'
    }
    return recommendations.get(priority, 'No specific recommendation available.')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': MODEL is not None,
        'scaler_loaded': SCALER is not None
    })


if __name__ == '__main__':
    # Initialize model on startup
    initialize_model()

    # Run Flask app
    print("Starting Flask API server...")
    print("API documentation available at: http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)

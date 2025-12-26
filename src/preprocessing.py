"""
Data Preprocessing Module
Handles feature scaling and feature engineering
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def standardize_features(data, features):
    """
    Standardize numerical features using StandardScaler

    Args:
        data (pd.DataFrame): Input dataframe
        features (list): List of features to standardize

    Returns:
        tuple: (processed data, fitted scaler)
    """
    data_copy = data.copy()
    scaler = StandardScaler()

    data_copy[features] = scaler.fit_transform(data_copy[features])

    print("Numerical features standardized successfully.")
    print("First 5 rows of the standardized data:")
    print(data_copy[features].head())

    return data_copy, scaler


def engineer_features(data):
    """
    Create new engineered features

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: Data with new features
    """
    data_copy = data.copy()

    # High child mortality indicator
    median_child_mort = data_copy['child_mort'].median()
    data_copy['High_Child_Mortality'] = (data_copy['child_mort'] > median_child_mort).astype(int)

    print(f"Median Child Mortality: {median_child_mort:.2f}")
    print("New feature 'High_Child_Mortality' created.")

    # Exports-Imports ratio
    data_copy['Exports_Imports_Ratio'] = data_copy['exports'] / data_copy['imports']

    print("New feature 'Exports_Imports_Ratio' created.")
    print("First 5 rows of the DataFrame with new features:")
    print(data_copy[['child_mort', 'High_Child_Mortality', 'exports', 'imports', 'Exports_Imports_Ratio']].head())

    return data_copy


def prepare_clustering_data(data, numerical_features):
    """
    Prepare data for clustering by selecting relevant features

    Args:
        data (pd.DataFrame): Input dataframe
        numerical_features (list): List of numerical features to use

    Returns:
        pd.DataFrame: Data prepared for clustering
    """
    data_for_clustering = data[numerical_features].copy()

    print("Data prepared for clustering:")
    print(data_for_clustering.head())

    return data_for_clustering


def preprocess_pipeline(data):
    """
    Complete preprocessing pipeline

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        tuple: (processed data, scaler, clustering data)
    """
    # Define numerical features
    numerical_features = ['child_mort', 'exports', 'health', 'imports',
                         'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']

    # Standardize features
    data_processed, scaler = standardize_features(data, numerical_features)

    # Engineer features
    data_processed = engineer_features(data_processed)

    # Prepare clustering data
    data_for_clustering = prepare_clustering_data(data_processed, numerical_features)

    return data_processed, scaler, data_for_clustering


if __name__ == "__main__":
    from data_loader import load_data

    data = load_data("../data/countries.csv")
    processed_data, scaler, clustering_data = preprocess_pipeline(data)

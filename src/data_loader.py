"""
Data Loading Module for Country Aid Clustering Project
Handles data loading and initial data inspection
"""

import pandas as pd
import numpy as np


def load_data(file_path):
    """
    Load country data from CSV file

    Args:
        file_path (str): Path to the CSV file

    Returns:
        pd.DataFrame: Loaded data
    """
    data = pd.read_csv(file_path)
    return data


def inspect_data(data):
    """
    Perform initial data inspection

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        dict: Dictionary containing data inspection results
    """
    inspection_results = {
        'shape': data.shape,
        'columns': list(data.columns),
        'dtypes': data.dtypes,
        'missing_values': data.isnull().sum(),
        'sample_data': data.head()
    }

    return inspection_results


def print_data_info(data):
    """
    Print comprehensive data information

    Args:
        data (pd.DataFrame): Input dataframe
    """
    print("="*50)
    print("DATA INFORMATION")
    print("="*50)
    print(f"\nDataset Shape: {data.shape}")
    print(f"\nColumns: {list(data.columns)}")
    print(f"\nData Types:\n{data.dtypes}")
    print(f"\nMissing Values:\n{data.isnull().sum()}")
    print(f"\nBasic Statistics:\n{data.describe()}")
    print("="*50)


if __name__ == "__main__":
    # Example usage
    data = load_data("C:/Users/Quadrant/Downloads/ClusteringCountriesAid/data/countries.csv")
    print_data_info(data)

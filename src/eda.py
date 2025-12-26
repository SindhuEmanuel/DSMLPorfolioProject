"""
Exploratory Data Analysis Module
Handles all EDA visualizations and analysis
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import os


def handle_outliers_winsorization(data, columns):
    """
    Detect and handle outliers using IQR method and winsorization

    Args:
        data (pd.DataFrame): Input dataframe
        columns (list): List of column names to process

    Returns:
        pd.DataFrame: Data with outliers handled
    """
    data_copy = data.copy()

    for col in columns:
        Q1 = data_copy[col].quantile(0.25)
        Q3 = data_copy[col].quantile(0.75)
        IQR = Q3 - Q1

        upper_bound = Q3 + 1.5 * IQR
        lower_bound = Q1 - 1.5 * IQR

        # Apply winsorization
        data_copy[col] = np.clip(data_copy[col], lower_bound, upper_bound)
        print(f"Winsorization applied to '{col}':")
        print(f"  Lower Bound: {lower_bound:.2f}")
        print(f"  Upper Bound: {upper_bound:.2f}")

    print("\nDescriptive statistics after winsorization:")
    print(data_copy[columns].describe())

    return data_copy


def plot_univariate_numerical(data, columns, save_plots=False):
    """
    Generate box plots and KDE plots for numerical variables

    Args:
        data (pd.DataFrame): Input dataframe
        columns (list): List of column names to plot
        save_plots (bool): If True, save plots to files instead of displaying
    """
    for col in columns:
        plt.figure(figsize=(12, 5))

        # Box Plot
        plt.subplot(1, 2, 1)
        sns.boxplot(y=data[col])
        plt.title(f'Box Plot of {col}')
        plt.ylabel(col)

        # KDE Plot
        plt.subplot(1, 2, 2)
        sns.kdeplot(x=data[col], fill=True)
        plt.title(f'KDE Plot of {col}')
        plt.xlabel(col)
        plt.ylabel('Density')

        plt.tight_layout()

        if save_plots:
            plt.savefig(f'plots/univariate_{col}.png', dpi=100, bbox_inches='tight')
            print(f"Saved plot: plots/univariate_{col}.png")

        plt.close()  # Close instead of show to avoid blocking


def plot_country_distribution(data, save_plots=False):
    """
    Create bar chart for country distribution

    Args:
        data (pd.DataFrame): Input dataframe
        save_plots (bool): If True, save plots to files instead of displaying
    """
    country_counts = data['country'].value_counts()

    print(f"Total number of unique countries: {len(country_counts)}")
    print("\nSample of unique country names (first 5 alphabetically sorted):")
    print(sorted(country_counts.index)[:5])
    print("\nSample of unique country names (last 5 alphabetically sorted):")
    print(sorted(country_counts.index)[-5:])

    # Skip plotting for non-interactive mode
    if save_plots:
        plt.figure(figsize=(15, 40))
        sns.barplot(x=country_counts.values, y=country_counts.index)
        plt.title('Distribution of Countries')
        plt.xlabel('Count')
        plt.ylabel('Country')
        plt.tight_layout()
        plt.savefig('plots/country_distribution.png', dpi=100, bbox_inches='tight')
        print("Saved plot: plots/country_distribution.png")
        plt.close()


def plot_correlation_matrix(data, save_plots=False):
    """
    Calculate and visualize correlation matrix

    Args:
        data (pd.DataFrame): Input dataframe
        save_plots (bool): If True, save plots to files instead of displaying
    """
    numerical_data = data.select_dtypes(include=np.number)
    correlation_matrix = numerical_data.corr()

    print("Correlation Matrix:")
    print(correlation_matrix)

    if save_plots:
        plt.figure(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
        plt.title('Correlation Matrix of Numerical Features')
        plt.savefig('plots/correlation_matrix.png', dpi=100, bbox_inches='tight')
        print("Saved plot: plots/correlation_matrix.png")
        plt.close()


def plot_bivariate_scatter(data, x_col, y_col, save_plots=False):
    """
    Create scatter plot for bivariate analysis

    Args:
        data (pd.DataFrame): Input dataframe
        x_col (str): X-axis column name
        y_col (str): Y-axis column name
        save_plots (bool): If True, save plots to files instead of displaying
    """
    if save_plots:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=data[x_col], y=data[y_col])
        plt.title(f'Scatter Plot: {x_col} vs. {y_col}')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.savefig(f'plots/scatter_{x_col}_vs_{y_col}.png', dpi=100, bbox_inches='tight')
        print(f"Saved plot: plots/scatter_{x_col}_vs_{y_col}.png")
        plt.close()


def perform_full_eda(data, save_plots=False):
    """
    Perform complete exploratory data analysis

    Args:
        data (pd.DataFrame): Input dataframe
        save_plots (bool): If True, save plots to files instead of displaying

    Returns:
        pd.DataFrame: Processed data
    """
    print("\n[EDA] Handling outliers...")
    # Handle outliers
    outlier_columns = ['child_mort', 'income', 'gdpp']
    data = handle_outliers_winsorization(data, outlier_columns)

    print("\n[EDA] Analyzing distributions...")
    # Univariate analysis
    numerical_columns = ['child_mort', 'income', 'life_expec']
    plot_univariate_numerical(data, numerical_columns, save_plots)

    print("\n[EDA] Analyzing country distribution...")
    # Country distribution
    plot_country_distribution(data, save_plots)

    print("\n[EDA] Computing correlation matrix...")
    # Correlation analysis
    plot_correlation_matrix(data, save_plots)

    print("\n[EDA] Bivariate analysis...")
    # Bivariate analysis
    plot_bivariate_scatter(data, 'health', 'life_expec', save_plots)

    print("\n[EDA] Complete!")
    return data


if __name__ == "__main__":
    from data_loader import load_data

    data = load_data("../data/countries.csv")
    data = perform_full_eda(data)

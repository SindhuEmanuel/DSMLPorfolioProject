"""
Statistical Analysis Module
Handles hypothesis testing and statistical analysis
"""

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, pearsonr


def test_child_mortality_income(data):
    """
    Test relationship between child mortality and income

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        dict: Test results
    """
    # Identify two groups based on median child mortality
    median_child_mort = data['child_mort'].median()

    high_child_mort_group = data[data['child_mort'] > median_child_mort]
    low_child_mort_group = data[data['child_mort'] <= median_child_mort]

    # Extract income for each group
    high_child_mort_income = high_child_mort_group['income']
    low_child_mort_income = low_child_mort_group['income']

    print(f"Median child mortality: {median_child_mort:.2f}")
    print(f"Number of countries with high child mortality: {len(high_child_mort_group)}")
    print(f"Number of countries with low child mortality: {len(low_child_mort_group)}")
    print("\nDescriptive statistics for income in high child mortality group:")
    print(high_child_mort_income.describe())
    print("\nDescriptive statistics for income in low child mortality group:")
    print(low_child_mort_income.describe())

    # Perform t-test
    t_stat, p_value = ttest_ind(high_child_mort_income, low_child_mort_income, equal_var=False)

    print(f"\nIndependent Samples t-test results:")
    print(f"  T-statistic: {t_stat:.4f}")
    print(f"  P-value: {p_value:.4f}")

    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        print(f"\nConclusion: Reject null hypothesis (p-value < {alpha})")
        print("There is a statistically significant difference in mean income between groups.")
    else:
        print(f"\nConclusion: Fail to reject null hypothesis (p-value >= {alpha})")
        print("No statistically significant difference in mean income between groups.")

    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'median_child_mort': median_child_mort,
        'high_group_size': len(high_child_mort_group),
        'low_group_size': len(low_child_mort_group)
    }


def test_health_life_expectancy(data):
    """
    Test relationship between health spending and life expectancy

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        dict: Test results
    """
    median_health = data['health'].median()

    high_health_spending_group = data[data['health'] > median_health]
    low_health_spending_group = data[data['health'] <= median_health]

    high_health_life_expec = high_health_spending_group['life_expec']
    low_health_life_expec = low_health_spending_group['life_expec']

    print(f"Median health spending: {median_health:.2f}")
    print(f"Number of countries with high health spending: {len(high_health_spending_group)}")
    print(f"Number of countries with low health spending: {len(low_health_spending_group)}")
    print("\nDescriptive statistics for life expectancy in high health spending group:")
    print(high_health_life_expec.describe())
    print("\nDescriptive statistics for life expectancy in low health spending group:")
    print(low_health_life_expec.describe())

    t_stat_health, p_value_health = ttest_ind(high_health_life_expec, low_health_life_expec, equal_var=False)

    print(f"\nIndependent Samples t-test results for health spending vs. life expectancy:")
    print(f"  T-statistic: {t_stat_health:.4f}")
    print(f"  P-value: {p_value_health:.4f}")

    alpha = 0.05
    if p_value_health < alpha:
        print(f"\nConclusion: Reject null hypothesis (p-value < {alpha})")
        print("Higher health spending is associated with significantly higher life expectancy.")
    else:
        print(f"\nConclusion: Fail to reject null hypothesis (p-value >= {alpha})")

    return {
        't_statistic': t_stat_health,
        'p_value': p_value_health,
        'median_health': median_health
    }


def test_fertility_income(data):
    """
    Test relationship between fertility and income

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        dict: Test results
    """
    median_total_fer = data['total_fer'].median()

    high_fertility_group = data[data['total_fer'] > median_total_fer]
    low_fertility_group = data[data['total_fer'] <= median_total_fer]

    high_fertility_income = high_fertility_group['income']
    low_fertility_income = low_fertility_group['income']

    print(f"Median total fertility rate: {median_total_fer:.2f}")
    print(f"Number of countries with high fertility rates: {len(high_fertility_group)}")
    print(f"Number of countries with low fertility rates: {len(low_fertility_group)}")

    print("\nDescriptive statistics for income in high fertility group:")
    print(high_fertility_income.describe())
    print("\nDescriptive statistics for income in low fertility group:")
    print(low_fertility_income.describe())

    t_stat_fer, p_value_fer = ttest_ind(high_fertility_income, low_fertility_income, equal_var=False)

    print(f"\nIndependent Samples t-test results for total fertility vs. income:")
    print(f"  T-statistic: {t_stat_fer:.4f}")
    print(f"  P-value: {p_value_fer:.4f}")

    # Correlation analysis
    correlation_coefficient, _ = pearsonr(data['total_fer'], data['income'])
    print(f"\nPearson Correlation between Total Fertility and Income: {correlation_coefficient:.4f}")

    return {
        't_statistic': t_stat_fer,
        'p_value': p_value_fer,
        'correlation': correlation_coefficient
    }


def test_inflation_gdpp(data):
    """
    Test relationship between inflation and GDP per capita

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        dict: Test results
    """
    median_inflation = data['inflation'].median()

    high_inflation_group = data[data['inflation'] > median_inflation]
    low_inflation_group = data[data['inflation'] <= median_inflation]

    high_inflation_gdpp = high_inflation_group['gdpp']
    low_inflation_gdpp = low_inflation_group['gdpp']

    print(f"Median inflation rate: {median_inflation:.2f}")
    print(f"Number of countries with high inflation rates: {len(high_inflation_group)}")
    print(f"Number of countries with low inflation rates: {len(low_inflation_group)}")

    print("\nDescriptive statistics for GDP per capita in high inflation group:")
    print(high_inflation_gdpp.describe())
    print("\nDescriptive statistics for GDP per capita in low inflation group:")
    print(low_inflation_gdpp.describe())

    t_stat_infl, p_value_infl = ttest_ind(high_inflation_gdpp, low_inflation_gdpp, equal_var=False)

    print(f"\nIndependent Samples t-test results for inflation vs. GDP per capita:")
    print(f"  T-statistic: {t_stat_infl:.4f}")
    print(f"  P-value: {p_value_infl:.4f}")

    correlation_coefficient_infl_gdpp, _ = pearsonr(data['inflation'], data['gdpp'])
    print(f"\nPearson Correlation between Inflation and GDP per capita: {correlation_coefficient_infl_gdpp:.4f}")

    return {
        't_statistic': t_stat_infl,
        'p_value': p_value_infl,
        'correlation': correlation_coefficient_infl_gdpp
    }


def perform_all_hypothesis_tests(data):
    """
    Perform all hypothesis tests

    Args:
        data (pd.DataFrame): Input dataframe

    Returns:
        dict: All test results
    """
    print("="*50)
    print("HYPOTHESIS TEST 1: Child Mortality vs Income")
    print("="*50)
    result1 = test_child_mortality_income(data)

    print("\n" + "="*50)
    print("HYPOTHESIS TEST 2: Health Spending vs Life Expectancy")
    print("="*50)
    result2 = test_health_life_expectancy(data)

    print("\n" + "="*50)
    print("HYPOTHESIS TEST 3: Fertility vs Income")
    print("="*50)
    result3 = test_fertility_income(data)

    print("\n" + "="*50)
    print("HYPOTHESIS TEST 4: Inflation vs GDP per Capita")
    print("="*50)
    result4 = test_inflation_gdpp(data)

    return {
        'child_mort_income': result1,
        'health_life_expec': result2,
        'fertility_income': result3,
        'inflation_gdpp': result4
    }


if __name__ == "__main__":
    from data_loader import load_data

    data = load_data("../data/countries.csv")
    results = perform_all_hypothesis_tests(data)

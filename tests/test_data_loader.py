"""
Unit tests for data_loader module
Example test file to demonstrate testing approach
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import load_data, inspect_data


class TestDataLoader:
    """Test cases for data loading functionality"""

    def test_load_data_returns_dataframe(self):
        """Test that load_data returns a pandas DataFrame"""
        # Create a temporary test CSV
        test_data = pd.DataFrame({
            'country': ['Country1', 'Country2'],
            'child_mort': [10.5, 20.3],
            'income': [5000, 10000]
        })

        test_file = 'test_data.csv'
        test_data.to_csv(test_file, index=False)

        try:
            result = load_data(test_file)
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 2
        finally:
            # Cleanup
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_inspect_data_returns_dict(self):
        """Test that inspect_data returns a dictionary"""
        test_data = pd.DataFrame({
            'country': ['Country1', 'Country2'],
            'child_mort': [10.5, 20.3],
            'income': [5000, 10000]
        })

        result = inspect_data(test_data)

        assert isinstance(result, dict)
        assert 'shape' in result
        assert 'columns' in result
        assert 'missing_values' in result

    def test_inspect_data_detects_missing_values(self):
        """Test that inspect_data correctly identifies missing values"""
        test_data = pd.DataFrame({
            'country': ['Country1', 'Country2', 'Country3'],
            'child_mort': [10.5, np.nan, 30.2],
            'income': [5000, 10000, np.nan]
        })

        result = inspect_data(test_data)

        assert result['missing_values']['child_mort'] == 1
        assert result['missing_values']['income'] == 1

    def test_inspect_data_correct_shape(self):
        """Test that inspect_data returns correct shape"""
        test_data = pd.DataFrame({
            'country': ['Country1', 'Country2'],
            'child_mort': [10.5, 20.3],
            'income': [5000, 10000]
        })

        result = inspect_data(test_data)

        assert result['shape'] == (2, 3)


class TestDataIntegrity:
    """Test cases for data integrity"""

    def test_no_duplicate_countries(self):
        """Test that there are no duplicate countries (if using real data)"""
        # This would be run with actual data
        # For now, just a placeholder
        pass

    def test_numerical_columns_are_numeric(self):
        """Test that numerical columns contain numeric data"""
        test_data = pd.DataFrame({
            'country': ['Country1', 'Country2'],
            'child_mort': [10.5, 20.3],
            'income': [5000, 10000]
        })

        assert pd.api.types.is_numeric_dtype(test_data['child_mort'])
        assert pd.api.types.is_numeric_dtype(test_data['income'])


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])

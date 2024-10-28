# tests/test_data_processor.py
import pytest
import pandas as pd
import os
import sqlite3
from pathlib import Path
import sys
sys.path.append('..')
from data_processor import DataProcessor
import pandas as pd


@pytest.fixture
def test_data_dir(tmp_path):
    """Create temporary directory with test data."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir


@pytest.fixture
def sample_csv(test_data_dir):
    """Create sample CSV file."""
    data = {
        "name": ["Bill Gates", "Carlos Slim Helu"],
        "rank": [1, 2],
        "year": [2014, 2014],
        "company_founded": [1975, 1990],
        "company_name": ["Microsoft", "Telmex"],
        "wealth_worth_in_billions": [76, 72],
    }
    df = pd.DataFrame(data)
    csv_path = test_data_dir / "billionaires.csv"
    df.to_csv(csv_path, index=False)
    return csv_path


def test_csv_file_detection(test_data_dir, sample_csv):
    processor = DataProcessor(test_data_dir)
    csv_files = processor.get_csv_files()
    assert len(csv_files) == 1
    assert csv_files[0].name == "billionaires.csv"


def test_data_validation(test_data_dir):
    processor = DataProcessor(test_data_dir)

    # Test valid data
    valid_data = pd.DataFrame(
        {
            "name": ["Test Person"],
            "rank": [1],
            "year": [2020],
            "company_founded": [2000],
            "company_name": ["Test Corp"],
            "wealth_worth_in_billions": [10.5],
        }
    )
    is_valid, issues = processor.validate_csv_data(valid_data)
    assert is_valid
    assert not issues

    # Test invalid data
    invalid_data = pd.DataFrame(
        {
            "name": ["Test Person"],
            "rank": ["invalid"],  # Invalid rank
            "year": [2020],
            "company_founded": [2000],
            "company_name": ["Test Corp"],
            "wealth_worth_in_billions": [-5],  # Invalid negative wealth
        }
    )
    is_valid, issues = processor.validate_csv_data(invalid_data)
    assert not is_valid
    assert len(issues) > 0


def test_data_cleaning(test_data_dir):
    """
    :param test_data_dir:
    :return:
    """
    processor = DataProcessor(test_data_dir)

    # Test data cleaning
    test_data = pd.DataFrame(
        {
            "name": ["Test Person"],
            "wealth_how_from_emerging": ["TRUE"],
            "wealth_how_was_founder": ["FALSE"],
            "rank": ["1"],
            "year": ["2020"],
        }
    )

    cleaned_data = processor.clean_data(test_data)

    # Debugging outputs
    print("Cleaned Data:")
    print(cleaned_data)
    print("Data Types:")
    print(cleaned_data.dtypes)

    # Assertions
    assert cleaned_data["wealth_how_from_emerging"].iloc[0] == True
    assert cleaned_data["wealth_how_was_founder"].iloc[0] == False
    assert pd.api.types.is_integer_dtype(
        cleaned_data["rank"]
    ), f"Rank is of type {type(cleaned_data['rank'].iloc[0])}"


def test_database_creation(test_data_dir, sample_csv):
    processor = DataProcessor(test_data_dir)
    success, error = processor.process_csv_to_db()

    assert success
    assert error is None
    assert (test_data_dir / "billionaires.db").exists()


if __name__ == "__main__":
    pytest.main(["-v"])

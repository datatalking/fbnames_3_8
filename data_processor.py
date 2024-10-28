import pandas as pd
import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple
import logging
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = sqlalchemy.orm.declarative_base()


class Billionaire(Base):
    __tablename__ = "billionaires"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rank = Column(Integer)
    year = Column(Integer)
    company_founded = Column(Integer)
    company_name = Column(String)
    company_relationship = Column(String)
    company_sector = Column(String)
    company_type = Column(String)
    demographics_age = Column(Integer)
    demographics_gender = Column(String)
    location_citizenship = Column(String)
    location_country_code = Column(String)
    location_gdp = Column(Float)
    location_region = Column(String)
    wealth_type = Column(String)
    wealth_worth_billions = Column(Float)
    wealth_how_category = Column(String)
    wealth_how_from_emerging = Column(Boolean)
    wealth_how_industry = Column(String)
    wealth_how_inherited = Column(String)
    wealth_how_was_founder = Column(Boolean)
    wealth_how_was_political = Column(Boolean)


class DataProcessor:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "billionaires.db"
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_csv_files(self) -> List[Path]:
        """Return list of CSV files in data directory."""
        return list(self.data_dir.glob("*.csv"))

    def validate_csv_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate CSV data for issues."""
        issues = []

        # Check for required columns
        required_columns = {
            "name",
            "rank",
            "year",
            "company_founded",
            "company_name",
            "wealth_worth_in_billions" # add in # TODO "wealth*worth*in*billions"
        }
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            issues.append(f"Missing required columns: {missing_columns}")

        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.any():
            issues.append(
                f"Null values found in columns: {null_counts[null_counts > 0].to_dict()}"
            )

        # Validate data types
        try:
            df["rank"] = pd.to_numeric(df["rank"])
            df["year"] = pd.to_numeric(df["year"])
            df["company_founded"] = pd.to_numeric(df["company_founded"])
            df["wealth_worth_in_billions"] = pd.to_numeric(
                df["wealth_worth_in_billions"]
            )
        except Exception as e:
            issues.append(f"Data type conversion error: {str(e)}")

        # Validate logical constraints
        if df["year"].min() < 1900 or df["year"].max() > 2100:
            issues.append("Invalid year values detected")

        if df["wealth_worth_in_billions"].min() < 0:
            issues.append("Negative wealth values detected")

        return len(issues) == 0, issues

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare data for database insertion."""
        df_clean = df.copy()

        # Clean column names
        df_clean.columns = df_clean.columns.str.replace(".", "_")

        # Convert boolean columns
        bool_columns = [
            "wealth_how_from_emerging",
            "wealth_how_was_founder",
            "wealth_how_was_political",
        ]
        for col in bool_columns:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].map({"TRUE": True, "FALSE": False})

        # Handle missing values with default placeholders
        null_replacements = {
            "company_name": "Unknown Company",
            "company_relationship": "Unknown Relationship",
            "company_sector": "Unknown Sector",
            "company_type": "Unknown Type",
            "demographics_gender": "Unknown Gender",
            "wealth_type": "Unknown Wealth Type",
            "wealth_how_category": "Unknown Category",
            "wealth_how_industry": "Unknown Industry",
        }
        for column, replacement in null_replacements.items():
            if column in df_clean.columns:
                missing_count = df_clean[column].isnull().sum()
                if missing_count > 0:
                    logger.info(
                        f"Filling {missing_count} missing values in '{column}' with '{replacement}'."
                    )
                    df_clean[column].fillna(replacement, inplace=True)

        # Convert numeric columns, ensuring nulls become NaN for database insertion
        numeric_columns = [
            "rank",
            "year",
            "company_founded",
            "demographics_age",
            "wealth_worth_in_billions",
        ]
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

        return df_clean

    def process_csv_to_db(self) -> Tuple[bool, Optional[str]]:
        """Process CSV files and load into SQLite database."""
        csv_files = self.get_csv_files()
        if not csv_files:
            return False, "No CSV files found in data directory"

        # Create the database table once before processing files
        Base.metadata.create_all(self.engine)

        # Process each CSV file
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                is_valid, issues = self.validate_csv_data(df)

                if not is_valid:
                    return False, f"Validation issues in {csv_file}: {issues}"

                df_clean = self.clean_data(df)

                # Create database connection and load data
                df_clean.to_sql(
                    "billionaires", self.engine, if_exists="replace", index=False
                )

                logger.info(f"Processing {csv_file} completed successfully.")

            except Exception as e:
                return False, f"Error processing {csv_file}: {str(e)}"

        return True, None  # Return None for the message if everything succeeds


if __name__ == "__main__":
    processor = DataProcessor(data_dir="data")
    success, message = processor.process_csv_to_db()
    if not success:
        logger.error(f"Failed to process data: {message}")
    else:
        logger.info(message)

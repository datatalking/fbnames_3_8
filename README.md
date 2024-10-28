# fbnames Data Directory

This directory contains the database files and CSV data for the billionaires analysis project.

## Contents
- `billionaires.db`: SQLite database file (auto-generated)
- `billionaires.csv`: Source CSV data file

## Database Plugin Configuration
1. Install Database Navigator plugin in PyCharm
2. Right-click on `billionaires.db` and select "Open Database"
3. Configure connection settings:
   - Name: billionaires
   - File: /path/to/data/billionaires.db
   - Driver: SQLite

Note: The `.db` file is gitignored. Run the data processor to generate it.


## Project Structure
"""
billionaires-analysis/
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
├── setup.cfg
├── README.md
├── src/
│   ├── __init__.py
│   ├── data_processor.py
│   ├── database.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_data_processor.py
│   └── test_data/
│       └── sample.csv
├── data/
│   ├── .gitkeep
│   └── README.md
└── .idea/
    ├── runConfigurations/
    │   └── pytest.xml
    └── dataSources/
        └── billionaires.xml
"""

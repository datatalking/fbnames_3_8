import os
import pandas as pd


def count_lines_of_code(directory):
    """Count lines of code in Python files in the specified directory."""
    total_lines = 0
    test_lines = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    test_lines += sum(
                        1
                        for line in lines
                        if line.strip() and line.strip().startswith("def test_")
                    )

    return total_lines, test_lines


def validate_data(directory):
    """Validate data in CSV files in the specified directory."""
    total_records = 0
    valid_records = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                filepath = os.path.join(root, file)
                df = pd.read_csv(filepath)
                total_records += len(df)

                # Example validation: Check if there are any NaN values
                valid_records += df.notnull().all(axis=1).sum()

    return total_records, valid_records


def calculate_coverage():
    code_directory = "your_project/"  # Adjust as necessary
    data_directory = os.path.join(code_directory, "data")

    # Count lines of code
    total_lines, test_lines = count_lines_of_code(code_directory)
    if total_lines > 0:
        code_coverage = (test_lines / total_lines) * 100
    else:
        code_coverage = 0

    # Validate data
    total_records, valid_records = validate_data(data_directory)
    if total_records > 0:
        data_coverage = (valid_records / total_records) * 100
    else:
        data_coverage = 0

    print(f"Code Coverage: {code_coverage:.2f}% ({test_lines}/{total_lines} lines)")
    print(
        f"Data Coverage: {data_coverage:.2f}% ({valid_records}/{total_records} records)"
    )


if __name__ == "__main__":
    calculate_coverage()

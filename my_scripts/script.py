import os
import pandas as pd


def process_csv(filepath):
    # Read CSV file into DataFrame
    df = pd.read_csv(filepath)

    # Get the first row for the header
    header = df.iloc[0]
    print(f"Headers in {filepath}:")
    print(header)

    # Try and parse types of the second row
    second_row = df.iloc[1]
    parsed_types = {col: type(val) for col, val in second_row.items()}
    print(f"/nTypes of the Second Row in {filepath}:")
    print(parsed_types)


# Iterate over all CSV files in a directory
for filename in os.listdir(
    "C:/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31"
):
    if filename.endswith(".csv"):  # if it's a CSV file
        process_csv(
            os.path.join(
                "C:/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31",
                filename,
            )
        )

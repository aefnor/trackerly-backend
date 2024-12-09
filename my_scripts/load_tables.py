import os
import pandas as pd
from sqlalchemy import create_engine

# Create an engine that stores data in Postgres DB
engine = create_engine("postgresql://fooduser:foodpass@localhost:5432/foodtracker")


def load_data(filepath, table_name):  # function to load csv file into PostgreSQL db
    df = pd.read_csv(filepath)  # Read CSV file into DataFrame
    print(filepath)
    # Rename columns to match your model
    df.rename(
        columns={
            "derivation code": "derivation_code",
            "derivation description": "derivation_description",
            "n.gid": "gid",
            "n.code": "code",
            "n.foodGroupId": "food_group_id",
            "n.description": "description",
        },
        inplace=True,
    )
    # df = df.drop_duplicates(subset=['fdc_id_of_sample_food'])
    df.to_sql(
        table_name,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=1000,
        method="multi",
    )


# for filename in os.listdir('C:/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31'): # Iterate over all CSV files in a directory
#     if filename.endswith('.csv'):  # if it's a CSV file
#         filepath = os.path.join('/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31', filename)
#         table_name = filename.split('.')[0] # table name will be the file name itself
#         load_data(filepath, table_name) # load data into postgres db

load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/retention_factor.csv",
    "retention_factor",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/sr_legacy_food.csv",
    "sr_legacy_food",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/input_food.csv",
    "input_food",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_attribute.csv",
    "food_attribute",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_attribute_type.csv",
    "food_attribute_type",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_category.csv",
    "food_category",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_component.csv",
    "food_component",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_nutrient.csv",
    "food_nutrient",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_nutrient_conversion_factor.csv",
    "food_nutrient_conversion_factor",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_nutrient_derivation.csv",
    "food_nutrient_derivation",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_nutrient_source.csv",
    "food_nutrient_source",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_portion.csv",
    "food_portion",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_protein_conversion_factor.csv",
    "food_protein_conversion_factor",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food_update_log_entry.csv",
    "food_update_log_entry",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/foundation_food.csv",
    "foundation_food",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/lab_method.csv",
    "lab_method",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/lab_method_code.csv",
    "lab_method_code",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/market_acquisition.csv",
    "market_acquisition",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/measure_unit.csv",
    "measure_unit",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/microbe.csv",
    "microbe",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/nutrient.csv",
    "nutrient",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/sample_food.csv",
    "sample_food",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/sub_sample_food.csv",
    "sub_sample_food",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/sub_sample_result.csv",
    "sub_sample_result",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/survey_fndds_food.csv",
    "survey_fndds_food",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/wweia_food_category.csv",
    "wweia_food_category",
)
load_data(
    "/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food.csv",
    "food",
)


engine.dispose()  # close engine once done

# acquisition_samples.csv
# agricultural_samples.csv
# branded_food.csv
# Download API Field
# Descriptions.xlsx
# fndds_derivation.csv
# fndds_ingredient_nutrient_
# value.xlsx
# food.csv
# food_attribute.csv
# food_attribute_type.csv
# food_calorie_conversion_fa
# ctor.csv
# food_category.csv
# food_component.csv
# food_nutrient.csv
# food_nutrient_conversion_f
# actor.csv
# food_nutrient_derivation.c
# sv
# food_nutrient_source.csv
# food_portion.csv
# food_protein_conversion_fa
# ctor.csv
# food_update_log_entry.csv
# foundation_food.csv
# input_food.csv
# lab_method.csv
# lab_method_code.csv
# lab_method_nutrient.csv
# market_acquisition.csv
# measure_unit.csv
# microbe.csv
# nutrient.csv
# retention_factor.csv
# sample_food.csv
# sr_legacy_food.csv
# sub_sample_food.csv
# sub_sample_result.csv
# survey_fndds_food.csv
# wweia_food_category.csv

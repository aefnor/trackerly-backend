import os
import pandas as pd
from sqlalchemy import create_engine

# Create an engine that stores data in Postgres DB
engine = create_engine('postgresql://fooduser:foodpass@localhost:5432/foodtracker')

def load_data(filepath, table_name): # function to load csv file into PostgreSQL db 
    df = pd.read_csv(filepath) # Read CSV file into DataFrame
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, chunksize=1000)

for filename in os.listdir('C:/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31'): # Iterate over all CSV files in a directory
    if filename.endswith('.csv'):  # if it's a CSV file
        filepath = os.path.join('/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31', filename) 
        table_name = filename.split('.')[0] # table name will be the file name itself
        load_data(filepath, table_name) # load data into postgres db

# load_data("/Users/Austin/Downloads/FoodData_Central_csv_2024-10-31/FoodData_Central_csv_2024-10-31/food.csv", "food")

engine.dispose() # close engine once done
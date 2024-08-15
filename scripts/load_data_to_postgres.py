import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection parameters
DATABASE_URL = 'postgresql://airflow:airflow@localhost:5436/airflow'

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Define the directory where the CSV files are located
data_directory = '/data'

# List of CSV files and their corresponding table names
csv_files = {
    'geolocation': 'geolocation.csv',
    'customers': 'customers.csv',
    'orders': 'orders.csv',
    'products': 'products.csv',
    'sellers': 'sellers.csv',
    'order_items': 'order_items.csv',
    'order_payments': 'order_payments.csv',
    'order_reviews': 'order_reviews.csv'
}

def load_csv_to_postgresql():
    for table_name, csv_file in csv_files.items():
        file_path = os.path.join(data_directory, csv_file)
        print(f"Loading data from {file_path} into table {table_name}...")
        
        try:
            df = pd.read_csv(file_path)  # Read data from CSV file
            df.to_sql(table_name, engine, if_exists='replace', index=False)  # Load data into PostgreSQL table
            print(f"Successfully loaded {csv_file} into {table_name} table.")
        except Exception as e:
            print(f"Error loading {csv_file} into {table_name}: {e}")

if __name__ == "__main__":
    load_csv_to_postgresql()


from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.bash import BashOperator
import os
from config import BIGQUERY_PROJECT_ID, GCS_BUCKET_NAME, BIGQUERY_DATASET, PG_FILEPATH




## BigQuery config variables
BQ_CONN_ID = "google_conn"
BQ_PROJECT = BIGQUERY_PROJECT_ID
BQ_DATASET = BIGQUERY_DATASET
BQ_BUCKET = GCS_BUCKET_NAME

## PostgreSQL config variables
PG_CONN_ID = "postgres_conn"
PG_SCHEMA = "ecommerce"  # The actual schema from the database.
PG_SCRIPT_FILEPATH = PG_FILEPATH


## List of tables to be pulled from postgresql
tables = [
    "customers",
    "orders",
    "order_items",
    "products",
    "sellers",
    "geolocation",
    "order_payments",
    "order_reviews"
]

default_args = {
    'owner': 'capstone',
    'start_date': datetime(2024, 7, 18),
    'retries': 1,   # Number of retries if a task fails
    'retry_delay': timedelta(minutes=5),   #Time between retries
}

dag = DAG(
    'postgresql_to_gbq_etl_load',
    default_args=default_args,
    description='An Airflow DAG for extracting tables from PostgreSQL and loading same into BigQuery',
    schedule_interval=None,
    catchup=False
)

# Add BashOperator to run the load_data_to_postgres.py script
create_postgresql_tables = BashOperator(
    task_id='create_postgresql_tables',
    bash_command=f'psql -h postgres -U airflow -d airflow -f {PG_SCRIPT_FILEPATH}/init.sql',
    dag=dag,
)

# Add BashOperator to run the load_data_to_postgres.py script
load_data_to_postgres = BashOperator(
    task_id='load_data_to_postgres',
    bash_command=f'python {PG_SCRIPT_FILEPATH}/load_data_to_postgres.py',
    dag=dag,
)

# Loop to create tasks for each table
for table in tables:
    csv_filename = f'{table}_data_dump_{datetime.now().strftime("%Y-%m-%d")}.csv'
    
    postgres_to_gcs = PostgresToGCSOperator(
        task_id = f'postgres_{table}_to_gcs',
        sql = f'SELECT * FROM "{PG_SCHEMA}"."{table}";',
        bucket = BQ_BUCKET,
        filename = csv_filename,
        export_format = 'CSV',
        postgres_conn_id = PG_CONN_ID,
        field_delimiter = ',',
        gzip = False,
        gcp_conn_id = BQ_CONN_ID,
        dag = dag,
    )

    gcs_to_bigquery = GCSToBigQueryOperator(
        task_id = f'bq_{table}_load_csv',
        bucket = BQ_BUCKET,
        source_objects = [csv_filename],
        destination_project_dataset_table = f"{BQ_PROJECT}.{BQ_DATASET}.{table}",
        max_bad_records=10,
        skip_leading_rows=1,
        create_disposition = 'CREATE_IF_NEEDED',
        write_disposition = "WRITE_TRUNCATE",
        gcp_conn_id = BQ_CONN_ID,
        dag = dag,
    )

    # Set the dependency chain
    create_postgresql_tables >> load_data_to_postgres >> postgres_to_gcs >> gcs_to_bigquery


# Allow previous dag objects to be and add BashOperator to run dbt models
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir .',
    dag=dag,
)

# Set dependency to run dbt after all tables have been loaded into BigQuery
for table in tables:
    globals()[f'bq_{table}_load_csv'] >> dbt_run
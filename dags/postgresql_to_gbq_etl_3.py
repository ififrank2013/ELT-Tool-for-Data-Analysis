from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.operators.bash_operator import BashOperator


## BigQuery config variables
BQ_CONN_ID = "google_conn"
BQ_PROJECT = "influential-sun-416018"
BQ_DATASET = "ecommerce"
BQ_BUCKET = "frank-altschool-bucket"

## Postgres config variables
PG_CONN_ID = "postgres_conn"
PG_SCHEMA = "public"  # The actual schema from the database.


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
    'postgresql_to_gbq_etl',
    default_args=default_args,
    description='An Airflow DAG for extracting tables from PostgreSQL and loading same into BigQuery',
    schedule_interval=None,
    catchup=False
)

load_data_to_postgres = BashOperator(
    task_id='load_data_to_postgres',
    bash_command='python C:/Users/olivc/OneDrive/Desktop/Frank/Altschool/resources/capstone-project/scripts',
    dag=dag,
)

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
        # schema_fields = [{"name": field, "type": "STRING", "mode": "NULLABLE"} for field in schema_fields],
        create_disposition = 'CREATE_IF_NEEDED',
        write_disposition = "WRITE_TRUNCATE",
        gcp_conn_id = BQ_CONN_ID,
        dag = dag,
    )

    load_data_to_postgres >> postgres_to_gcs >> gcs_to_bigquery
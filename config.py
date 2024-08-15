import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_CONN_ID = os.getenv('POSTGRES_CONN_ID')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
BIGQUERY_PROJECT_ID = os.getenv('PROJECT_ID')
BIGQUERY_DATASET = os.getenv('DATASET_ID')
PG_FILEPATH = os.getenv('PG_SCRIPT_FILEPATH')

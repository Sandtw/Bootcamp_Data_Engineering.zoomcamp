from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(retries=3)
def ingest_data(dataset_url):
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def transform_data(df):
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    return df

@task(log_prints=True)
def export_data_local(df, color, dataset_file):
    path = Path(f"data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path

@task(log_prints=True)
def export_data_gcs(path):
    gcs_block = GcsBucket.load("zoomp-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return path

@flow("Ingest file to GCS")
def etl_web_to_gcs():
    color = "yellow"
    year = 2021
    month = 1
    dataset_file=f"{color}_tripdata_{year}-{month:02}"
    dataset_url  = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = ingest_data(dataset_url)
    df_clean = transform_data(df)
    path = export_data_local(df_clean, color, dataset_file)
    export_data_gcs(path)

if __name__ == "__main__":
    etl_web_to_gcs()

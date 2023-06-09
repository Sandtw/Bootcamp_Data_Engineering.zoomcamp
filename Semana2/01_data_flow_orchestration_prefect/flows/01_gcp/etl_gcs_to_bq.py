from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

@task(name="Extract GCP parquet to local",retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    gcs_path = f"{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoomp-gcs")
    gcs_block.get_directory(from_path = gcs_path, local_path = f"../../data/yellow/")
    return Path(f"../../data/yellow/{gcs_path}")

@task(name="Transform parquet")
def transform(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df['passenger_count'].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df

@task(name="Upload Bigquery")
def write_bq(df: pd.DataFrame) -> None:
    gcp_credentials_block = GcpCredentials.load("zoomp-gcp-creds")  
    df.to_gbq(
        destination_table = "dzoomcamp.rides",
        project_id = "root-blueprint-379706",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow(name= "Ingest parquet GCS to Bigquery")
def etl_gcs_to_bq():
    color = "yellow"
    year = 2021
    month = 1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)

if __name__ == "__main__":
    etl_gcs_to_bq()
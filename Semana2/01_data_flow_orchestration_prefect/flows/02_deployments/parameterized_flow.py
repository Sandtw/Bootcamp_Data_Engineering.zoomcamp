from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta, datetime

@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def ingest_data(dataset_url:str) -> pd.DataFrame:
    df = pd.read_csv(dataset_url)
    return df

@task(log_prints=True)
def transform_data(df = pd.DataFrame) -> pd.DataFrame:
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task(log_prints=True)
def export_data_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    path = Path(f"../../data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path

@task(log_prints=True)
def export_data_gcs(path: Path,to_path: Path) -> None:
    gcs_block = GcsBucket.load("zoomp-gcs")
    gcs_block.upload_from_path(from_path=path, to_path = to_path)
    return 

@flow(name = "Ingest file to GCS")
def etl_web_to_gcs(year: int, month: int, color : str) -> None:

    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = ingest_data(dataset_url)
    df_clean = transform_data(df)
    path = export_data_local(df_clean, color, dataset_file)
    to_path = Path(f"{dataset_file}.parquet")
    export_data_gcs(path, to_path)

@flow()
def etl_parent_flow(months: list[int] = [1,2], year: int = 2021, color: str = "yellow"):
    for month in months:
        etl_web_to_gcs(year, month, color)

if __name__ == "__main__":
    color = 'yellow'
    months = [1,2,3]
    year = 2021

    etl_parent_flow(months, year, color)
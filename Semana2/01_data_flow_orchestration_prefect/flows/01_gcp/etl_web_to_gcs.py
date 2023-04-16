from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint

@task(retries=3)
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
def etl_web_to_gcs() -> None:
    color = 'yellow'
    year = 2021
    month = 1
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = ingest_data(dataset_url)
    df_clean = transform_data(df)
    path = export_data_local(df_clean, color, dataset_file)
    to_path = Path(f"{dataset_file}.parquet")
    export_data_gcs(path, to_path)

if __name__ == "__main__":
    etl_web_to_gcs()
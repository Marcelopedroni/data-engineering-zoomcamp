import pandas as pd
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from os import getcwd



@task(retries=3)
def fetch(dataset_url:str) -> pd.DataFrame:
  """Read taxi data from web into pandas DataFrame"""
  
  df = pd.read_csv(dataset_url)
  return df


@task(log_prints=True)
def clean(df = pd.DataFrame) -> pd.DataFrame:
  """Fix data type issues"""

  df['tpep_pickup_datetime']  = pd.to_datetime(df['tpep_pickup_datetime'])
  df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
  df = df[df['passenger_count'] != 0]

  return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
  """Write DataFrame out locally as parquet file"""

  path = Path(f"{getcwd()}/data/{color}/{dataset_file}.parquet")
  df.to_parquet(path, compression="gzip")

  return path

@task()
def write_gcs(path: Path, to_path: str) -> None:
  """Uploading local parquet file to GCS"""
  gcs_block = GcsBucket.load("zoom-gcs")
  gcs_block.upload_from_path(from_path=path,to_path=to_path)


@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
  """Main ETL function"""

  dataset_file = f"{color}_tripdata_{year}-{month:02}"
  dataset_url  = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"
  to_path = f"data/{color}/{dataset_file}.parquet"

  df = fetch(dataset_url)
  if color != "green":
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
  else:
    path = write_local(df, color, dataset_file)
  write_gcs(path, to_path)

@flow()
def etl_parent_flow(
  months: list[int] = [1,2,3,4,5,6,7,8,9,10,11,12], year: int = 2021, color: str = "green"
):
  for month in months:
    etl_web_to_gcs(year, month, color)

if __name__ == "__main__":
  color = "yellow"
  months = [7]
  year = 2021
  etl_parent_flow(months, year, color)

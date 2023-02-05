#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time


def main(params):
  ingest_ny_taxi_data(params)
  ingest_zones(params)


def ingest_ny_taxi_data(params):
  user = params.user
  password = params.password
  host = params.host
  port = params.port
  db = params.db
  table_name = params.table_name
  url = params.url
  
  if url.endswith('.csv.gz'):
    csv_name = 'output.csv.gz'
  else:
    csv_name = 'output.csv'
  
  # download the csv file
  os.system(f"wget {url} -O {csv_name}")

  engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

  df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

  df = next(df_iter)

  df.tpep_pickup_datetime =  pd.to_datetime(df.tpep_pickup_datetime)
  df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

  df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
  df.to_sql(name=table_name, con=engine, if_exists='append')

  while True:

    try:
      t_start = time()
      df = next(df_iter)
      df.tpep_pickup_datetime =  pd.to_datetime(df.tpep_pickup_datetime)
      df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
      df.to_sql(name=table_name, con=engine, if_exists='append')

      t_end = time()

      print('inserted another chunk..., took %.3f seconds' %(t_end - t_start))

    except StopIteration:
      print("Finished ingesting ny taxi data into the postgres database")
      break


def ingest_zones(params):
  user            = params.user
  password        = params.password
  host            = params.host
  port            = params.port
  db              = params.db
  url_zone        = params.url_zone
  table_name_zone = params.table_name_zone
  csv_name_zone   = 'taxi+_zone_lookup.csv'

  os.system(f"wget {url_zone} -O {csv_name_zone}")

  engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

  # Ingest and create table zone lookup on Postgres database
  df_zone = pd.read_csv(csv_name_zone)
  df_zone.to_sql(name=table_name_zone, con=engine, if_exists='replace')
  print("Finished ingesting ny taxi zones data into the postgres database")

  return True

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Ingest CSV's data to Postgres")

  parser.add_argument('--user',       required=True, help='user name for postgres')
  parser.add_argument('--password',   required=True, help='password for postgres')
  parser.add_argument('--host',       required=True, help='host for postgres')
  parser.add_argument('--port',       required=True, help='port for postgres')
  parser.add_argument('--db',         required=True, help='database name for postgres')
  parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
  parser.add_argument('--url',        required=True, help='url of the csv file')
  parser.add_argument('--url_zone',        required=True, help='url of the csv file')
  parser.add_argument('--table_name_zone', required=True, help='name of the table where we will write the results to')

  args = parser.parse_args()

  main(args)

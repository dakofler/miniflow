"""Data ingestion job."""

from logging import getLogger

from pandas import DataFrame, read_csv

from helpers.db import get_postgres_conn

DATA_URL = "https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv"
LOGGER = getLogger(__file__)


def ingest_data() -> None:
    raw_data = _fetch_data()
    LOGGER.info("Fetched data")
    processed_data = _process_data(raw_data)
    LOGGER.info("Processed data")
    _save_data(processed_data)
    LOGGER.info("Saved data")


def _fetch_data() -> DataFrame:
    df = read_csv(DATA_URL, header=0, sep=",")
    return df


def _process_data(df: DataFrame) -> None:
    df["encoded_col"] = df["variety"].astype("category").cat.codes
    return df


def _save_data(df: DataFrame) -> None:
    conn = get_postgres_conn("postgres")
    df.to_sql("iris", conn, if_exists="replace", index=True)

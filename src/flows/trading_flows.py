from prefect import flow, task

from src.data_source.data_source_api import DataFetcher

df_ = DataFetcher()


@task
def fetch_data_crypto():
    df_.fetch_crypto()


@task
def fetch_data_stock():
    df_.fetch_stock()


@flow(log_prints=True)
def fetch_data_flow():
    fetch_data_crypto()
    fetch_data_stock()

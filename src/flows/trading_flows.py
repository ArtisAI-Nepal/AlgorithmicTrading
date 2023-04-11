from prefect import flow, task

from src.data_source.data_source_api import DataFetcher


@task
def fetch_data_task(msg):
    df_ = DataFetcher()
    df_.main_process()


@flow(log_prints=True)
def fetch_data_flow():
    fetch_data_task("test")

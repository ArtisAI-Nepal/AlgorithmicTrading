"""crypto data update happens here"""
import os

import pandas as pd
import yfinance as yf


def get_data(script, start_date, end_date):
    data = yf.download(script, start=start_date, end=end_date)
    return data


def initiate_extraction(script, start_date, end_date):
    try:
        data = get_data(script=script,
                        start_date=start_date,
                        end_date=end_date)
    except Exception as exe:
        print(exe)
        data = pd.DataFrame(columns=[
            "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"
        ])

    prev_data = get_pre_data(script)
    recent = pd.concat([prev_data, data])
    output_path = os.path.join(os.getcwd(), "data", "stocks")
    recent.to_csv(os.path.join(output_path, f"{script}.csv"))


def get_pre_data(script):
    data_dir = os.path.join(os.getcwd(), "data")
    required_file = os.path.join(data_dir, f"{script}.csv")
    if os.path.exists(required_file):
        return pd.read_csv(required_file)
    else:
        return pd.DataFrame(columns=[
            "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"
        ])


if __name__ == "__main__":
    initiate_extraction(script="SPY",
                        start_date="2020-01-01",
                        end_date="2023-04-06")

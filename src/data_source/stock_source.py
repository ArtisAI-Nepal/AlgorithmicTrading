"""crypto data update happens here"""
import os

import pandas as pd
import yfinance as yf


class StockDataFetcher:

    def __init__(self, script: list):
        self.script = script

    def get_data(self, single_script, start_date, end_date):
        data = yf.download(single_script, start=start_date, end=end_date)
        return data

    def initiate_extraction(self, start_date, end_date):
        try:
            data = [
                self.get_data(single_script=script,
                              start_date=start_date,
                              end_date=end_date) for script in self.script
            ]
        except Exception as exe:
            print(exe)
            data = pd.DataFrame(columns=[
                "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"
            ])

        for i_, single_script in enumerate(self.script):
            prev_data = self.get_pre_data(single_script)
            recent = pd.concat([prev_data, data[i_]])
            output_path = os.path.join(os.getcwd(), "data", "stocks")
            recent.to_csv(os.path.join(output_path, f"{single_script}.csv"))

    def get_pre_data(self, single_script):
        data_dir = os.path.join(os.getcwd(), "data")
        required_file = os.path.join(data_dir, f"{single_script}.csv")
        if os.path.exists(required_file):
            return pd.read_csv(required_file)
        else:
            return pd.DataFrame(columns=[
                "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"
            ])


if __name__ == "__main__":
    sdata = StockDataFetcher(script=[
        "SPY",
        "AMZN",
        "TSLA",
        "AMD",
        "NVDA",
        "AAPL",
        "BAC",
        "QQQ",
        "IWM",
        "MSFT",
        "NFLX",
    ])
    sdata.initiate_extraction(start_date="2020-01-01", end_date="2023-04-11")

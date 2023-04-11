import os

import pandas as pd
import requests

# data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')


class CryptoDataFetcher:

    def __init__(self,
                 coin="bitcoin",
                 vs_currency="usd",
                 days=10,
                 interval="daily"):
        """Fetches Data for Crypto

        Args:
            coin (str, optional): name of the coin to fetch data for. Defaults to 'bitcoin'.
            vs_currency (str, optional): currency we want to see valuation on. Defaults to 'usd'.
            days (int, optional): how many days ago o data you need. Defaults to 10.
            interval (str, optional): freqency of data to be fetched. Defaults to 'daily'.
        """
        self.vs_currency = vs_currency
        self.coin = coin
        self.url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
        self.params = {
            "vs_currency": vs_currency,
            "days": days,
            "interval": interval
        }

    def get_response(self):
        """Makes a get request to get data from API

        Returns:
            dict: dictionary of data based on the params
        """
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            SystemExit(0)
        return data

    def make_dataframe(self):
        """Makes a dataframe from the data fetched

        Returns:
            pd.Dataframe: pandas dataframe of the data in flat format
        """
        data = self.get_response()
        df = pd.DataFrame({
            "timestamp":
            [pd.to_datetime(i[0], unit="ms") for i in data["prices"]],
            "prices": [i[1] for i in data["prices"]],
            "market_caps": [i[1] for i in data["market_caps"]],
            "total_volumes": [i[1] for i in data["total_volumes"]],
        })
        # df['timestamp'] = df['timestamp'].apply(lambda x: x.timestamp())
        return df

    def create_csv(self):
        """Make a new csv or appends a new data if already exists"""
        data_folder = os.path.join(os.getcwd(), "data")
        csv_file = os.path.join(data_folder, "crypto", self.coin + ".csv")
        mode = "a" if os.path.isfile(csv_file) else "w"
        if mode == "a":
            self.params["days"] = 1

        df = self.make_dataframe()
        df.to_csv(csv_file,
                  mode=mode,
                  header=not os.path.isfile(csv_file),
                  index=False)


if __name__ == "__main__":
    instance = CryptoDataFetcher()
    instance.create_csv()

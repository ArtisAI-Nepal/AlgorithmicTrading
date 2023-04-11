"""data update happens here"""
from src.data_source.crypto_source import CryptoDataFetcher
from src.data_source.stock_source import StockDataFetcher


class DataFetcher:

    def __init__(self):
        pass

    def fetch_stock(self):
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
        sdata.initiate_extraction(start_date="2020-01-01",
                                  end_date="2023-04-06")

    def fetch_crypto(self):
        instance = CryptoDataFetcher(coin="bitcoin", days="3650")
        instance.create_csv()

    def main_process(self):
        self.fetch_crypto()
        self.fetch_stock()
        print("stock / crypto data fetch")


if __name__ == "__main__":
    _df_ = DataFetcher()
    _df_.main_process()

"""data update happens here"""
from crypto_source import CryptoDataFetcher


class DataFetcher:

    def __init__(self):
        pass

    def fetch_stock(self):
        pass

    def fetch_crypto(self):
        instance = CryptoDataFetcher(coin="bitcoin", days="3650")
        instance.create_csv()

    def main_process(self):
        # :TODO: this method will run daily using prefect.
        self.fetch_crypto()
        self.fetch_stock()
        print("stock / crypto data fetch")


if __name__ == "__main__":
    _df_ = DataFetcher()
    _df_.main_process()
    # :TODO: test cases.

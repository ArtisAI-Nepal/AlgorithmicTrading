"""data update happens here"""

class DataFetcher:
    def __init__(self):
        pass

    def fetch_stock(self):
        pass

    def fetch_crypto(self):
        pass

    def main_process(self):
        #:TODO: this method will run daily using prefect.
        self.fetch_crypto()
        self.fetch_stock()
        print("stock / crypto data fetch")


if __name__ == "__main__":
    _df_ = DataFetcher()
    _df_.main_process() 
    # :TODO: test cases. 
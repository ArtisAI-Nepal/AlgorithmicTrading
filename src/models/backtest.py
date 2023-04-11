from datetime import datetime

import pandas as pd

from src.indicators.indicator import Indicators


class BackTester:
    def __init__(self, data_source_type="crypto", equity="bitcoin"):
        self.initial_balance = 100
        self.initial_date = 0
        self.data_source_type = data_source_type
        self.equity = equity
        self.indicator = Indicators()

    def run_test(self):
        start_date = datetime(2018, 1, 1)
        end_date = datetime(2022, 12, 31)
        dates = pd.date_range(start_date, end_date)
        shares = [self.equity]
        if self.data_source_type == "crypto":
            self.indicator.colname = "prices"
            self.indicator.base_dir += "/crypto"
            price_df = self.indicator.get_data(
                symbols=shares, dates=dates, addSPY=False, index_col="timestamp"
            )
        else:
            self.indicator.base_dir += "/stocks"
            self.indicator.colname = "Adj Close"
            price_df = self.indicator.get_data(symbols=shares, dates=dates)
        price_df = price_df.fillna(method="ffill").fillna(method="bfill")
        # import pdb
        # pdb.set_trace()
        _ = self.indicator.MACD(price_df, symbol=shares[0])


if __name__ == "__main__":
    bt = BackTester()
    bt.run_test()

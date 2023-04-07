import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd


class Indicators:
    def __init__(self):
        sys.path.append(os.getcwd())
        self.base_dir = "./src/data"  # fix later with config
        self.colname = "Adj Close"
        pass

    def symbol_to_path(self, symbol):
        return os.path.join(self.base_dir, f"{str(symbol)}.csv")

    def get_data(self, dates, symbols, addSPY=True):
        df = pd.DataFrame(index=dates)
        if addSPY and "SPY" not in symbols:
            symbols = ["SPY"] + list(symbols)

        for symbol in symbols:
            df_temp = pd.read_csv(
                self.symbol_to_path(symbol),
                index_col="Date",
                parse_dates=True,
                usecols=["Date", self.colname],
                na_values=["nan"],
            )
            df_temp = df_temp.rename(columns={self.colname: symbol})
            df = df.join(df_temp)
            if symbol == "SPY":  # drop dates SPY did not trade
                df = df.dropna(subset=["SPY"])
        return df

    def MACD(self, price_df, symbol):
        ema_12 = price_df.ewm(span=12, adjust=False).mean()
        ema_26 = price_df.ewm(span=26, adjust=False).mean()
        macd_df = ema_12 - ema_26
        signal_df = macd_df.ewm(span=9, adjust=False).mean()
        histogram = macd_df - signal_df
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(macd_df, label="MACD")
        ax.plot(signal_df, label="signal")

        label_status = False
        for i in range(len(histogram)):
            if histogram[symbol][i] >= 0:
                if not label_status:
                    ax.bar(
                        histogram.index[i],
                        histogram[symbol][i],
                        color="green",
                        label="Histogram",
                    )
                    label_status = True
                else:
                    ax.bar(histogram.index[i], histogram[symbol][i], color="green")
            else:
                if not label_status:
                    ax.bar(
                        histogram.index[i],
                        histogram[symbol][i],
                        color="red",
                        label="Histogram",
                    )
                    label_status = True
                else:
                    ax.bar(histogram.index[i], histogram[symbol][i], color="red")

        plt.title("MACD")
        plt.xlabel("Date")
        plt.ylabel("MACD values")
        plt.legend()
        plt.grid()
        plt.savefig("./macd.png")
        plt.clf()
        return macd_df

    def main_process(self):
        start_date = datetime(2008, 1, 1)
        end_date = datetime(2009, 12, 31)
        shares = ["AMZN"]
        dates = pd.date_range(start_date, end_date)
        price_df = self.get_data(symbols=shares, dates=dates)
        price_df = (
            price_df.drop("SPY", axis=1).fillna(method="ffill").fillna(method="bfill")
        )
        _ = self.MACD(price_df, symbol=shares[0])


if __name__ == "__main__":
    ind = Indicators()
    ind.main_process()
# AlgorithmicTrading ❯ python src/indicators/indicator.py

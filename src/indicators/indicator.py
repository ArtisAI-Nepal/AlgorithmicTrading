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

    def BBP(self, price_df, window_days=14):
        price_df = price_df / price_df.iloc[0]
        std_df = price_df.rolling(window=window_days, min_periods=window_days).std()
        sma_df = price_df.rolling(window=window_days, min_periods=window_days).mean()
        upper_band_df = sma_df + 2.0 * std_df
        lower_band_df = sma_df - 2.0 * std_df
        bbp_df = (price_df - lower_band_df) / (upper_band_df - lower_band_df)
        plt.figure(figsize=(14, 8))
        plt.plot(upper_band_df, label="upper band", color="red")
        plt.plot(lower_band_df, label="lower band", color="red")
        plt.plot(price_df, label="price", color="blue")
        plt.plot(sma_df, label="SMA", color="green")
        plt.xlabel("Date")
        plt.ylabel("Normalized Price")
        plt.title(f"Upper/ lower Bollinger Bands [ window = {window_days} days ]")
        plt.legend()
        plt.grid()
        plt.savefig(f"./BBwindow{window_days}.png")
        plt.clf()

        plt.figure(figsize=(14, 8))
        plt.plot(bbp_df, label="BBP", color="red")
        plt.xlabel("Date")
        plt.ylabel("Normalized Price")
        plt.title(f"Bollinger Bands Percentage (BBP) [ window = {window_days} days ]")
        plt.legend()
        plt.grid()
        plt.axhline(1.0, linestyle="--", linewidth=2)
        plt.axhline(0.0, linestyle="--", linewidth=2)
        plt.savefig(f"./BBPwindow{window_days}.png")
        plt.clf()
        return bbp_df

    def SMA(self, price_df, window_days=14):
        price_df = price_df / price_df.iloc[0]
        sma_df = price_df.rolling(window=window_days, min_periods=window_days).mean()
        price_per_sma_df = price_df / sma_df
        plt.figure(figsize=(14, 8))
        plt.plot(price_df, label="price")
        plt.plot(sma_df, label="SMA")
        plt.plot(price_per_sma_df, label="price/SMA")
        plt.xlabel("Date")
        plt.ylabel("Normalized Price")
        plt.title(
            f"Price Vs Simple Moving Average(SMA) Vs Price/SMA [ window = {window_days} days ]"
        )
        plt.legend()
        plt.axhline(1.0, linestyle="--", linewidth=2, color="purple")
        plt.grid()
        plt.savefig(f"./smawindow{window_days}.png")
        plt.clf()
        return sma_df

    def CCI(self, price_df, window_days=14):
        # std_df = price_df.rolling(window=window_days, min_periods=window_days).std()
        sma_df = price_df.rolling(window=window_days, min_periods=window_days).mean()
        mean_deviation = price_df.rolling(window=window_days).apply(
            lambda x: pd.Series(x).mad()
        )
        cci_df = (price_df - sma_df) / (0.015 * mean_deviation)

        plt.figure(figsize=(14, 8))
        ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=5, colspan=1)
        ax1.plot(price_df, label="price", color="blue")
        ax1.set_title("share price")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price")
        ax1.legend()
        ax1.grid()

        ax2 = plt.subplot2grid((10, 1), (6, 0), rowspan=4, colspan=1)
        ax2.plot(cci_df, label="CCI", color="red")
        ax2.set_title(f"Commodity Channel Index, [ window = {window_days} days ]")
        ax2.axhline(200, linestyle="--", linewidth=2)
        ax2.axhline(-150, linestyle="--", linewidth=2)
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Price")
        ax2.legend()
        ax2.grid()

        plt.savefig(f"./cci{window_days}.png")
        plt.clf()
        return cci_df

    def momentum(self, price_df, window_days=14):
        mtm_df = price_df - price_df.shift(window_days)
        plt.figure(figsize=(14, 8))
        ax1 = plt.subplot2grid((10, 1), (0, 0), rowspan=5, colspan=1)
        ax1.plot(price_df, label="price", color="blue")
        ax1.set_title("share price")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price")
        ax1.legend()
        ax1.grid()

        ax2 = plt.subplot2grid((10, 1), (6, 0), rowspan=4, colspan=1)
        ax2.plot(mtm_df, label="Momentum", color="red")
        ax2.set_title(f"Momentum (Mtm) [ window = {window_days} days ]")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("MTM")
        ax2.legend()
        ax2.grid()

        plt.savefig(f"./mtm{window_days}.png")
        plt.clf()

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
        _ = self.BBP(price_df)
        _ = self.SMA(price_df)
        _ = self.CCI(price_df)
        _ = self.momentum(price_df)


if __name__ == "__main__":
    ind = Indicators()
    ind.main_process()
# AlgorithmicTrading ❯ python src/indicators/indicator.py

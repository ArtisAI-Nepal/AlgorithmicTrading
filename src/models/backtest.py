import os
from datetime import datetime

import cv2
import matplotlib.pyplot as plt
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
        start_date = datetime(2021, 1, 1)
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
        macd, signal = self.indicator.MACD(price_df, symbol=shares[0])
        self.create_video(dates, macd, signal, price_df, shares[0])

    def create_video(self, dates, macd_df, signal_df, price_df, symbol):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter("macd_video.mp4", fourcc, 10.0, (800, 600))

        # # Define colors
        # green = (0, 255, 0)
        # red = (0, 0, 255)
        # white = (255, 255, 255)

        for date in dates:
            macd_value = macd_df.loc[date][0]
            signal_value = signal_df.loc[date][0]

            # Initialize plot
            fig, (ax1, ax2) = plt.subplots(
                nrows=2, figsize=(8, 8), gridspec_kw={"height_ratios": [3, 1]}
            )
            (price_line,) = ax1.plot(price_df.index, price_df[symbol], label="Price")
            fig.suptitle("MACD Indicator", fontsize=16)
            # Set axis labels and legends
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Price")

            # Plot MACD line
            (macd_line,) = ax2.plot(macd_df.index, macd_df[symbol], label="MACD")

            # Plot signal line
            (signal_line,) = ax2.plot(
                signal_df.index, signal_df[symbol], label="Signal"
            )

            # Add buy and sell annotations for crossovers
            if macd_value > signal_value:
                ax2.scatter(
                    date, macd_value, s=100, marker="^", color="green", label="Buy"
                )
            elif macd_value < signal_value:
                ax2.scatter(
                    date, macd_value, s=100, marker="v", color="red", label="Sell"
                )

            ax2.set_xlabel("Date")
            ax2.set_ylabel("MACD Value")
            ax1.legend(loc="upper left")
            ax2.legend(loc="upper left")

            fig.savefig("temp.png")

            # Load image and write to video
            img = cv2.imread("temp.png")
            out.write(img)

            # Close plot and delete image
            plt.close(fig)
            cv2.waitKey(1)
            cv2.destroyAllWindows()

        # Release video writer and delete temporary image
        out.release()
        os.remove("temp.png")


if __name__ == "__main__":
    bt = BackTester()
    bt.run_test()

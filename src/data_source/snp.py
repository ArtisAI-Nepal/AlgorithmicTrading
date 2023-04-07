import yfinance as yf
import pandas as pd
import os

def get_data(script, start_date, end_date):
  data = yf.download(script, start=start_date, end=end_date)
  return data

def initiate_extraction():
    #data = get_data(script="SPY", start_date = "2010-01-01", end_date = "2023-04-06")
    prev_data=get_pre_data("SPY")
    print(prev_data)
    new_df = pd.DataFrame.append(other, ignore_index=False, verify_integrity=False, sort=None)


def get_pre_data(script):
    data_dir = os.path.join(os.getcwd(),'data')
    required_file = os.path.join(data_dir,f'{script}.csv')
    print(required_file)
    if os.path.exists(required_file):
        return pd.read_csv(required_file)
    else:
        return pd.DataFrame()



print(initiate_extraction())
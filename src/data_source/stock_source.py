"""crypto data update happens here"""
import yfinance as yf
import pandas as pd
import os

def get_data(script, start_date, end_date):
  data = yf.download(script, start=start_date, end=end_date)
  return data

def initiate_extraction(script,start_date,end_date ):
    data = get_data(script=script, start_date=start_date, end_date=end_date)
    prev_data = get_pre_data(script)
    recent = pd.concat([prev_data, data])
    recent.to_csv(f'{script}.csv')
def get_pre_data(script):
    data_dir = os.path.join(os.getcwd(),'data')
    required_file = os.path.join(data_dir,f'{script}.csv')
    print(required_file)
    if os.path.exists(required_file):
        return pd.read_csv(required_file)
    else:
        return pd.DataFrame(columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

if __name__ == '__main__':
    initiate_extraction(script="SPY", start_date = "2020-01-01", end_date = "2023-04-06")
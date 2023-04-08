import os
import requests
import pandas as pd

data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')

class CryptoDataFetcher(object):

    def __init__(self, coin='bitcoin', vs_currency='usd', days=10, interval='daily') :
        """Initialze required variables
        """
        self.vs_currency = vs_currency
        self.coin = coin
        self.url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart'
        self.params = {
            'vs_currency': vs_currency,
            'days': days,
            'interval': interval
        }

    def get_response(self):
        """Get response from the API
        """
        response = requests.get(self.url, params=self.params)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f'Request failed with status code {response.status_code}')
            SystemExit(0)
        return data

    def make_dataframe(self):
        data = self.get_response()
        df = pd.DataFrame({
                'timestamp': [pd.to_datetime(i[0], unit='ms') for i in data['prices']],
                'prices': [i[1] for i in data['prices']],
                'market_caps': [i[1] for i in data['market_caps']],
                'total_volumes': [i[1] for i in data['total_volumes']]})
        df['timestamp'] = df['timestamp'].apply(lambda x: x.timestamp())
        return df

    def create_csv(self):
        df = self.make_dataframe()
        csv_file = os.path.join(data_folder, self.coin + '.csv')
        mode=('a' if os.path.isfile(csv_file) else 'w')
        df.to_csv(
            csv_file,
            mode=mode,
            header= not os.path.isfile(csv_file),
            index=False)

if __name__=='__main__':
    instance = CryptoDataFetcher()
    instance.create_csv()
import requests
import pandas as pd

class CryptoDataFetcher(object):

    def __init__(self, coin='bitcoin', vs_currency='usd', days=10, interval='daily') :
        """Initialze required variables
        """
        self.vs_currency = vs_currency
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
        print(response)
        if response.status_code == 200:
            data = response.json()
        else:
            print(f'Request failed with status code {response.status_code}')
        return data

if __name__=='__main__':
    instance = CryptoDataFetcher()
    data = instance.get_response()
    #need to make it a proper csv
    # print this to get the data, will be implementing it toomorrow
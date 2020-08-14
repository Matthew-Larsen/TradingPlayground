import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class APITester():
    def __init__(self):
        self.API_KEY = "pk_c7bc26bfc80b40b4ae8981833be927f1"
        self.base_url = 'https://cloud.iexapis.com/stable/'
        self.sandbox_url = 'https://sandbox.iexapis.com/stable/'
        self.symbol = 'AAPL'
        self.df = pd.DataFrame(columns=['date', 'minute', 'label', 'high', 'low', 'open', 'close', 'average', 'volume',
                                        'notional', 'numberOfTrades'])

    def load(self, days=30):
        date = (datetime.now() - timedelta(days=days)).date()
        now = datetime.today().date()
        while date <= now:
            print(f"getting data from {date.strftime('%Y-%m-%d')}")
            r = requests.get(url=self.base_url+"stock/" + self.symbol + "/intraday-prices?token=" + self.API_KEY +
                                 "&exactDate=" + date.strftime("%Y%m%d"))
            try:
                j = r.json()
            except:
                print(r)
                print(r.content)
                return
            for row in j:
                series = pd.Series(row)
                self.df = self.df.append(series, ignore_index=True)
            date = date + timedelta(days=1)
        return self.df

    def SMA(self, date_num):
        sma = [None]*date_num
        for i in range(date_num, len(self.df)):
            sma.append(self.df[i-date_num:i]['high'].mean())
        self.df['SMA'+str(date_num)] = sma


if __name__ == '__main__':
    api = APITester().load()
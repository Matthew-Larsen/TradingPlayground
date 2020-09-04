import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

class GenericStrategy():
    def __init__(self, symbol='NVDA'):
        self.API_KEY = "pk_c7bc26bfc80b40b4ae8981833be927f1"
        self.base_url = 'https://cloud.iexapis.com/stable/'
        self.sandbox_url = 'https://sandbox.iexapis.com/stable/'
        self.symbol = symbol
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

    def find_cross(self, short_col_name, long_col_name):
        shortOverLong = True
        buys = []
        sells = []
        for day in range(len(self.df)):
            if np.isnan(self.df[long_col_name][day]) or not self.df[long_col_name][day] or \
                    np.isnan(self.df[short_col_name][day]) or not self.df[short_col_name][day]:
                buys.append(None)
                sells.append(None)
            elif self.df[short_col_name][day] >= self.df[long_col_name][day]:
                if not shortOverLong and len([x for x in buys if x]) > 0:
                    shortOverLong = True
                    sells.append(self.df['average'][day])
                    buys.append(None)
                else:
                    buys.append(None)
                    sells.append(None)
            elif self.df[short_col_name][day] < self.df[long_col_name][day]:
                if shortOverLong:
                    shortOverLong = False
                    buys.append(self.df['average'][day])
                    sells.append(None)
                else:
                    buys.append(None)
                    sells.append(None)
            else:
                buys.append(None)
                sells.append(None)
        print(len(buys))
        print(len(self.df))
        self.df[short_col_name + '/' + long_col_name + '/buys'] = buys
        self.df[short_col_name + '/' + long_col_name + '/sells'] = sells

    def basic_graph(self, short_col, long_col):
        plt.plot(self.df['average'], label='ground')
        plt.plot(self.df[short_col], label=short_col)
        plt.plot(self.df[long_col], label=long_col)
        plt.scatter(x=range(len(self.df)), y=self.df[short_col+'/'+long_col+'/'+'buys'], label='buys', color='green')
        plt.scatter(x=range(len(self.df)), y=self.df[short_col + '/' + long_col + '/' + 'sells'], label='sells',
                    color='red')
        plt.legend()
        plt.show()
    def calculate_profit(self, buys_col, sells_col, investment):
        owned = 0
        init_investment = investment
        for i in range(len(self.df)):
            if self.df[buys_col][i] and not np.isnan(self.df[buys_col][i]):
                owned = investment // self.df[buys_col][i]
                #print(f"buying {owned} at {self.df['average'][i]} each")
                investment -= (owned * self.df['average'][i])

            elif self.df[sells_col][i] and not np.isnan(self.df[sells_col][i]) and owned > 0:
                #print(f"Selling {owned} at {self.df['average'][i]} each")
                investment += (owned * self.df['average'][i])
                owned = 0
        if owned > 0:
            investment += (owned * self.df['average'][-1])

        return investment - init_investment

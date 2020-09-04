import requests
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

from Model.GenericStrategy import GenericStrategy


class SMACrossoverStrategy(GenericStrategy):
    def __init__(self, symbol='NVDA'):
        super().__init__(symbol)

    def get_sma(self, date_num):
        self.df['SMA'+str(date_num)] = self.df['average'].rolling(window=date_num, min_periods=1).mean()

    def backtest(self, short, long, days=30, graph=False, investment=1000):
        if len(self.df) == 0:
            self.load(days)

        short_name = 'SMA' + str(short)
        long_name = 'SMA' + str(long)

        if short_name not in self.df.columns:
            self.get_sma(short)
        if long_name not in self.df.columns:
            self.get_sma(long)

        buys = short_name+'/'+long_name+'/'+'buys'
        sells = short_name+'/'+long_name+'/'+'sells'

        if buys not in self.df.columns or sells not in self.df.columns:
            self.find_cross(short_col_name=short_name, long_col_name=long_name)

        if graph:
            self.basic_graph(short_col=short_name, long_col=long_name)

        profit = self.calculate_profit(buys, sells, investment=investment)
        print(f"""Profit of {profit} given initial investment of {investment} on ticker {self.symbol} using strategy sma crossover on {short} / {long}""")
        return profit





if __name__ == '__main__':
    api = SMACrossoverStrategy()
    api.load()
    api.backtest(25, 100, graph=False, investment=2000)
    api.backtest(50, 200, graph=False, investment=2000)
    api.backtest(100, 400, graph=False, investment=2000)
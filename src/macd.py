import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

INIT_SHORT_EMA = 12
INIT_LONG_EMA = 26
INIT_SIGNAL_EMA = 9

class MACDStrategy:
    def __init__(self, prices: pd.Series) -> None:
        self.prices = prices
        self.df = self.compute_macd(INIT_LONG_EMA, INIT_SHORT_EMA, INIT_SIGNAL_EMA)
        self.buy, self.sell, self.macd_signal = self.macd_strategy()
        self.position = self.get_position()

    def compute_macd(self, slow: int, fast: int, signal_len: int):
        prices = self.prices
        ewma_slow = prices.ewm(span=slow, adjust=False, min_periods=slow).mean()
        ewma_fast = prices.ewm(span=fast, adjust=False, min_periods=fast).mean()
        macd = ewma_fast - ewma_slow
        signal = macd.ewm(span=signal_len, adjust=False, min_periods=signal_len).mean()
        hist = macd - signal
        df = pd.concat([macd, signal, hist], join='inner', keys=['macd', 'signal', 'hist'], axis=1)
        return df

    def macd_strategy(self):
        prices = self.prices
        data = self.df
        buy = []
        sell = []
        macd_signal = []
        signal = 0

        for i in range(len(data)):
            # if data['macd'][i] > data['signal'][i] and data['rsi'][i-1] <= 35:
            if data['macd'][i] > data['signal'][i]:
                if signal != 1:
                    buy.append(prices[i])
                    sell.append(np.nan)
                    signal = 1
                    macd_signal.append(signal)
                else:
                    buy.append(np.nan)
                    sell.append(np.nan)
                    macd_signal.append(0)

            # elif data['macd'][i] < data['signal'][i] and data['rsi'][i-1] >= 70:
            elif data['macd'][i] < data['signal'][i]:
                if signal != -1:
                    buy.append(np.nan)
                    sell.append(prices[i])
                    signal = -1
                    macd_signal.append(signal)
                else:
                    buy.append(np.nan)
                    sell.append(np.nan)
                    macd_signal.append(0)
            else:
                buy.append(np.nan)
                sell.append(np.nan)
                macd_signal.append(0)

        return buy, sell, macd_signal

    def get_position(self):
        prices = self.prices
        macd_signal = self.macd_signal

        position = []
        for i in range(len(macd_signal)):
            if macd_signal[i] > 1:
                position.append(0)
            else:
                position.append(1)
        
        for i in range(len(prices)):
            if macd_signal[i] == 1:
                position[i] = 1
            elif macd_signal[i] == -1:
                position[i] = 0
            else:
                position[i] = position[i-1]

        return position

    # plot macd
    def plot_macd(self):
        prices = self.prices
        buy = self.buy
        sell = self.sell

        macd = self.df['macd']
        signal = self.df['signal']
        hist = self.df['hist']

        plt.style.use('fivethirtyeight')
        ax1 = plt.subplot2grid((8,1), (0,0), rowspan = 5, colspan = 1)
        ax2 = plt.subplot2grid((8,1), (5,0), rowspan = 3, colspan = 1)
        ax1.plot(prices.index, buy, marker = '^', color = 'green', \
            markersize = 10, label = 'BUY SIGNAL', linewidth = 0)
        ax1.plot(prices.index, sell, marker = 'v', color = 'red', \
            markersize = 10, label = 'BUY SIGNAL', linewidth = 0)

        ax1.plot(prices, linewidth = 2)
        ax2.plot(macd, color = 'grey', linewidth = 1.5, label = 'MACD')
        ax2.plot(signal, color = 'skyblue', linewidth = 1.5, label = 'SIGNAL')

        for i in range(len(prices)):
            if hist[i] < 0:
                ax2.bar(prices.index[i], hist[i], color = '#ef5350')
            else:
                ax2.bar(prices.index[i], hist[i], color = '#26a69a')
        plt.legend(loc='lower right')
        plt.show()
    
    def get_return_rates(self, investment_value):
        cp_returns = np.diff(self.prices)
        num_of_stocks = np.floor(investment_value / self.prices[0])
        strategy_ret = []

        for i in range(len(cp_returns)):
            returns = cp_returns[i] * self.position[i] * num_of_stocks
            strategy_ret.append(returns)
        
        total_investment = round(np.sum(strategy_ret), 2)
        profit_percentage = np.floor((total_investment / investment_value) * 100)
        return total_investment, profit_percentage

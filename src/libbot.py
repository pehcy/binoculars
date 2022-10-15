from turtle import position
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Callable
import os

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

INIT_SHORT_EMA = 12
INIT_LONG_EMA = 26
INIT_SIGNAL_EMA = 9

# Split dataframe into several blocks then apply function on them
def run_blocks(data: pd.Series, size: int, func: Callable) -> list:
    return np.array([func(data.iloc[i:size+i]) for i in range(0, len(data), size)])

def compute_macd(price: pd.Series, slow: int, fast: int, signal_len: int):
    ewma_slow = price.ewm(span=slow, adjust=False, min_periods=slow).mean()
    ewma_fast = price.ewm(span=fast, adjust=False, min_periods=fast).mean()
    macd = ewma_fast - ewma_slow
    signal = macd.ewm(span=signal_len, adjust=False, min_periods=signal_len).mean()
    hist = macd - signal
    df = pd.concat([macd, signal, hist], join='inner', keys=['macd', 'signal', 'hist'], axis=1)
    return df

def compute_rsi(data: pd.Series):
    gain = np.extract(data > 0, data)
    loss = np.extract(data < 0, data)

    avg_gain = np.mean(gain)
    avg_loss = np.mean(np.absolute(loss))

    result = 100 - 100 / (1 + avg_gain / avg_loss)
    return result

# second step for RSI calculation
def compute_rsi_next(temp_gain, temp_loss, current_gain, current_loss, step):
    """
     temp_gain:     the average gain from previous window, type: float64
     temp_gain:     the average loss from previous window, should be positive numbers
     step:          number of period(or lag) for rolling RSI
    """
    
    wavg_gain = (temp_gain * step) + current_gain
    wavg_loss = (temp_loss * step) + current_loss
    return 100 - 100 / (1 + wavg_gain / wavg_loss)

# plot macd
def plot_macd(
        prices: pd.Series, 
        macd: pd.Series, 
        signal: pd.Series, 
        hist: pd.Series,
        buy: pd.Series,
        sell: pd.Series
    ):
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

def rsi_strategy(rsi):
    return

def macd_strategy(prices, data):
    buy = []
    sell = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
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

def create_position(close_prices, macd_signal):
    position = []
    for i in range(len(macd_signal)):
        if macd_signal[i] > 1:
            position.append(0)
        else:
            position.append(1)
    
    for i in range(len(close_prices)):
        if macd_signal[i] == 1:
            position[i] = 1
        elif macd_signal[i] == -1:
            position[i] = 0
        else:
            position[i] = position[i-1]

    return position


if __name__ == '__main__':
    df = pd.read_csv(os.path.join(os.getcwd(), 'src/data/adausdt.csv'))

    df['returns'] = df['Close'] - df['Close'].shift(-1)
    df.dropna(inplace=True)

    # Sample of BTC/USDT close price from time 0 to 200
    sample_close_prices = df['Close']

    fr_macd = compute_macd(sample_close_prices, INIT_LONG_EMA, INIT_SHORT_EMA, INIT_SIGNAL_EMA)
    
    print('Calculating MACD...')
    buy_prices, sell_prices, macd_signal = macd_strategy(df['Close'], fr_macd)
    plot_macd(sample_close_prices, fr_macd['macd'], fr_macd['signal'], \
        fr_macd['hist'], buy_prices, sell_prices)
    plt.show()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Callable

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
    ewma_long = price.ewm(span=slow, adjust=False).mean()
    ewma_short = price.ewm(span=fast, adjust=False).mean()
    macd = ewma_long - ewma_short
    signal = macd.ewm(span=signal_len, adjust=False).mean()
    hist = macd - signal
    df = pd.concat([macd, signal, hist], join='inner', axis=1)
    return df

# compute exponential moving average
def compute_ema(data: pd.Series):
    n = len(data)
    alpha = 2 / (1 + n)
    w = [(1 - alpha) ** i for i in range(n)]

    ema = np.dot(w, data) / np.sum(w)
    return ema

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

def plot_run_chart():
    return

def rsi_strategy():
    return

if __name__ == '__main__':
    df = pd.read_csv('../src/data/btcusdt.csv')
    df['returns'] = df['Close'] - df['Close'].shift(-1)
    df.dropna(inplace=True)
    rsi_windows = np.array(run_blocks(df['returns'], 28))
    plt.plot(rsi_windows)
    plt.show()
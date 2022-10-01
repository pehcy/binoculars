import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

RSI_PERIOD = 28
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

def compute_rsi(data: pd.Series):
    gain = np.extract(data > 0, data)
    loss = np.extract(data < 0, data)

    avg_gain = np.mean(gain)
    avg_loss = np.mean(np.absolute(loss))

    print(f'The average gain is: {avg_gain:.6f}')
    print(f'The average loss is: {avg_loss:.6f}')
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

def rsi_strategy():
    return
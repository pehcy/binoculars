import numpy as np

def get_pnl(gain, loss):
    """
     Calculate profit and loss of the portfolio
    """
    return np.mean(gain) / np.mean(loss)

def get_sharpe_ratio():
    return

def get_sortino():
    return
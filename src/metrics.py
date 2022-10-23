import numpy as np

def get_pnl(gain, loss):
    """
     Calculate profit and loss of the portfolio
    """
    return np.mean(gain) / np.mean(loss)

def get_sharpe_ratio(gain, risk_free_interest_rate):
    return (np.mean(gain) - risk_free_interest_rate) / np.std(gain)

def get_sortino_ratio():
    return
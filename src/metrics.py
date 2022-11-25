import numpy as np

def get_pnl(gain, loss):
    """
     Calculate profit and loss of the portfolio
    """
    return np.sum(gain) / len(gain)

def get_sharpe_ratio(gain, risk_free_interest_rate):
    return (np.mean(gain) - risk_free_interest_rate) / np.std(gain)

def get_sortino_ratio(gain, risk_free_interest_rate):
    return (np.mean(gain) - risk_free_interest_rate) / np.std(gain)

def hausdorff_distance(actual, predict):
    a = (actual['Open'] + actual['Close']) / 2 \
        - (predict['Open'] + predict['Close']) / 2
    b = (actual['Open'] - actual['Close']) / 2 \
        - (predict['Open'] - predict['Close']) / 2
    rmseh2 = np.mean(np.square(np.abs(a) + np.abs(b)))
    return np.sqrt(rmseh2)
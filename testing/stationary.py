import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

'''
Test stationary of time series with augmented Dickey-Fuller test
:Null Hypothesis            H0: The time series is staionary.
:Alternative Hypothesis     H1: The time series has trend.
:p-value                    Reject H0 if p-value > 0.05
'''
def test_stationarity(data: pd.DataFrame, period: int):
    rolling_mean = data.rolling(period).mean()
    rolling_std = data.rolling(period).std()

    # Plot rolling statistics
    fig = plt.figure(figsize=(10,6))
    original = plt.plot(data, color='#d0cbc9', label='Original', alpha=0.5)
    mean = plt.plot(rolling_mean, color='#f84c1e', label='Rolling mean', alpha=0.6, linewidth=2.85)
    std_dev = plt.plot(rolling_std, color='#595d66', label='Rolling std', linewidth=2.85)
    plt.legend(loc='best')
    plt.title('Rolling mean & std deviation')
    plt.show()

    # use Akaike Information Criterion
    test = adfuller(data, autolag='AIC')
    print('Augmented Dickey-Fuller test summary:')
    output = pd.Series(test[:4], index=[
                'Test statistic',
                'p-value',
                'Num of lags used',
                'Num of observations'])
    
    for key, value in test[4].items():
        output[f'Critical value ({key})'] = value
    print(output)


import numpy as np
import pandas as pd

class SMAStrategy:
    '''
        :params
        period: int
    '''
    
    def __init__(self, datas: pd.DataFrame, smaperiod: int) -> None:
        self._amount = None
        
        self._close_prices = []
        self._datas = datas
        self._period = smaperiod
        self.sma1 = datas.rolling(self._period).mean()
    
    def next(self):
        if self._close_prices[0] > self.sma:
            # buy order here
            print('Long stock with price: ...')
            self._amout = None
        else:
            # short order
            print('Short stock with price: ...')
            self._amount = 0

class RSIStrategy:
    def __init__(self) -> None:
        pass
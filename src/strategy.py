import pandas as pd
import pickle

class Strategy:
    def __init__(self) -> None:
        self.sma = 0
    
    def fetch_ticker(self, ):
        return {
            'symbol': symbol
        }
import sqlite3
import time
import websocket
import datetime
import numpy as np
import pandas as pd
import duck
# import db

import asyncio
from multiprocessing import Pool

def on_message(ws, message):
    print(str(datetime.datetime.now()) + ': ')
    print(type(message))
    duck.log_duckdb(message)
    # db.log_db(message)

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print('### Closed ###' + close_msg)

def stream_kline(symbol: str):
    websocket.enableTrace(False)
    # socket = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_{interval}'
    socket = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@depth'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

duck.init_duckdb()

if __name__ == '__main__':
    print("start server")
    stream_kline('bnbbtc')

    #df[cols] = np.where(df[cols] > 0, 1, 0)
    #df['direction'] = np.where(df['log_returns'] > 0, 1, -1)

    #stream_kline('SOLUSDT', '1m')
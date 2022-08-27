import sqlite3
import time
import websocket
import datetime
import numpy as np
import pandas as pd
import db

import asyncio
from multiprocessing import Pool
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def on_message(ws, message):
    print(str(datetime.datetime.now()) + ': ')
    print(message)
    db.log_db(message)

def on_error(ws, error):
    print(error)

def on_close(close_msg):
    print('### Closed ###' + close_msg)

def stream_kline(symbol, interval):
    websocket.enableTrace(False)
    socket = f'wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_{interval}'
    ws = websocket.WebSocketApp(socket,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

db.init_db()

if __name__ == '__main__':
    #pool =  Pool()
    con = sqlite3.connect("streaming.db")
    df = pd.read_sql_query("SELECT * FROM Solusdt", con)

    cols = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']

    # generate log returns
    df["log_returns"] = np.log(df["Close"] / df["Close"].shift(1))
    
    cols = []
    minutes2shift = [1, 2, 3, 4, 5]
    for lag in minutes2shift:
        if 'log_returns' in df:
            col = 'lag_{}'.format(lag)
            df[col] = df['log_returns'].shift(lag)
            cols.append(col)
    df = df.dropna()
    df[cols] = np.where(df[cols] > 0, 1, 0)
    df['direction'] = np.where(df['log_returns'] > 0, 1, -1)

    split = int(len(df) * 0.80)
    train = df.iloc[:split].copy()
    model = SVC(C=1, kernel='poly', degree=3)
    model.fit(train[cols], train['direction'])

    print(df)
    print(accuracy_score(train['direction'], model.predict(train[cols])))

    test = df.iloc[split:].copy()
    test['position'] = model.predict(test[cols])
    print(accuracy_score(test['direction'], test['position']))



    #df[cols] = np.where(df[cols] > 0, 1, 0)
    #df['direction'] = np.where(df['log_returns'] > 0, 1, -1)

    #stream_kline('SOLUSDT', '1m')
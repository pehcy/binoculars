from fileinput import close
import json
import sqlite3
import uuid

def init_db():
    connect = sqlite3.connect('streaming.db')
    cur = connect.cursor()

    cur.execute(''' CREATE TABLE IF NOT EXISTS Solusdt
                (Id text, Symbol text, Interval text, Close real, High real, Low real, Timestamp integer)''')
    connect.commit()

def log_db(message):
    parsed = json.loads(message)
    k = parsed['k']
    id = str(uuid.uuid4().hex)
    symbol = k['s']
    interval = k['i']
    close = float(k['c'])
    high =  float(k['h'])
    low = float(k['l'])
    time = int(k['t'])

    print("log: ")
    print("symbol: " + symbol)
    print("interval: " + interval)
    print("close: " + str(close))
    print("high: " + str(high))
    print("low: " + str(low))
    print("time: " + str(time))

    row = (id, symbol, interval, close, high, low, time)
    connect = sqlite3.connect('streaming.db')
    cursor = connect.cursor()
    cmd = "insert into Solusdt (Id, Symbol, Interval, Close, High, Low , Timestamp) values (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(cmd, row)
    connect.commit()
    connect.close()
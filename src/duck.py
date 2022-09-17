import duckdb
import json

"""
Duckdb 🦆 is an in-process SQL OLAP 
database management system. This file used to 
handle duckdb functions.
"""

def init_duckdb():
    con = duckdb.connect("diffbook.duckdb")
    con.execute(''' CREATE TABLE IF NOT EXISTS 
                    t_diff_depth (d HUGEINT, first HUGEINT, final HUGEINT)
                ''')
    con.execute(''' CREATE TABLE IF NOT EXISTS
                    ask (d STRING, p DOUBLE, q INTEGER)
                ''')
    con.execute(''' CREATE TABLE IF NOT EXISTS
                    bid (d STRING, p DOUBLE, q INTEGER)
                ''')

def log_duckdb(message: json):
    parsed = json.loads(message)
    asks = parsed["a"]
    bids = parsed["b"]
    timestmp = parsed["E"]
    first = parsed["U"]
    last = parsed["u"]

    con = duckdb.connect("diffbook.duckdb")
    cmd = {
        'insert_depth': "INSERT INTO t_diff_depth VALUES (?, ?, ?)",
        'insert_a': "INSERT INTO t_diff_depth VALUES (?, ?, ?)"
    }

    con.execute("INSERT INTO t_diff_depth VALUES (?, ?, ?)", [timestmp, first, last])
    print(parsed)

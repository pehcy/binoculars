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
                    ask (d HUGEINT, p DOUBLE, q INTEGER)
                ''')
    con.execute(''' CREATE TABLE IF NOT EXISTS
                    bid (d HUGEINT, p DOUBLE, q INTEGER)
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
        'insert_a': "INSERT INTO ask VALUES (?, ?, ?)",
        'insert_b': "INSERT INTO bid VALUES (?, ?, ?)"
    }

    con.execute(cmd["insert_depth"], [timestmp, first, last])

    if len(asks) > 0:
        for [p, v] in asks:
            con.execute(cmd["insert_a"], [timestmp, p, v])
    
    if len(bids) > 0:
        for [p, v] in bids:
            con.execute(cmd["insert_b"], [timestmp, p, v])

    print(parsed)

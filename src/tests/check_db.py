import sqlite3

con = sqlite3.connect('streaming.db')
cur = con.cursor()
cmd = "select * from Solusdt"
cur.execute(cmd)

rows = cur.fetchall()

for row in rows:
    print(row)

con.close()
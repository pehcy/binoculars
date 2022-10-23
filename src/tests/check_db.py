import duckdb

con = duckdb.connect("diffbook.duckdb")
query = con.execute("SELECT * FROM ask").fetch_df()
print(query)
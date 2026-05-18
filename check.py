import sqlite3

con = sqlite3.connect("easyjob.db")
rows = con.execute("SELECT * FROM users").fetchall()
print(rows)

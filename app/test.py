import sqlite3


con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("select * from workdays WHERE date=?", ("2021-12-08",))
result = (cur.fetchall())
con.close()
print(result)

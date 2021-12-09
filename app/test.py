import sqlite3


con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute(
    "select * from workdays WHERE date=? ORDER BY id DESC LIMIT 1", ("2021-12-07",))
result = (cur.fetchall())
con.close()
print(result)

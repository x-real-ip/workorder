import sqlite3


def query(database_name, date):
    """Return values from database based on date"""
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute("select * from workdays WHERE date=?", (date,))
    result = (cur.fetchone())
    con.close()
    return result

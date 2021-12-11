import sqlite3


def query(database, date):
    """Return values from database based on date"""
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(
        "select * from workdays WHERE date=? ORDER BY id DESC LIMIT 1", (date,))
    result = (cur.fetchone())
    con.close()
    return result

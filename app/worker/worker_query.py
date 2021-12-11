import sqlite3


def query(database_name, date):
    """Return values from database based on date"""
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute(
        "select * from workdays WHERE date=? ORDER BY id DESC LIMIT 1", (date,))
    result = (cur.fetchone())
    con.close()
    return result

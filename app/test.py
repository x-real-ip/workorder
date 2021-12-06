import sqlite3

# Create a SQL connection to our SQLite database
con = sqlite3.connect("workdays.db")

cur = con.cursor()

# # The result of a "cursor.execute" can be iterated over by row
# for row in cur.execute('SELECT * FROM workdays WHERE date="2021-12-09";'):
#     print(row)


# Return all results of query
cur.execute('SELECT * FROM workdays WHERE date="2021-12-09"')
result = cur.fetchone()
print(result[2])
# Be sure to close the connection
con.close()

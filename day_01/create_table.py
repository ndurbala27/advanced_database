import sqlite3 as sql

conn = sql.connect('people.db')
curr = conn.cursor()

curr.execute(
    """CREATE TABLE persons(
             name TEXT,
             age INTEGER,
             address TEXT)"""
)

conn.commit()
curr.close()
conn.close()
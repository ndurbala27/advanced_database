import sqlite3 as sql

conn = sql.connect('people.db')
curr = conn.cursor()
rows = curr.execute("SELECT * FROM persons").fetchall()
if rows:
    print(f"{'PERSONS':-^30}")
    for i, row in enumerate(rows, 1):
        name, age, city = row
        print(f"{i} | {name.title():<9}| {age} | {city}")
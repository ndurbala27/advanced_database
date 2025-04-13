import sqlite3 as sql
from pprint import pprint as pprint
import json

conn = sql.connect('people.db')
curr = conn.cursor()
rows = curr.execute("SELECT * FROM persons").fetchall()

plist = []

if rows:
    for i, row in enumerate(rows, 1):
        pdct = {}
        name, age, city = row
        pdct['Name'] = name.title()
        pdct['Age'] = age
        pdct['City'] = city.title()
        plist.append(pdct)

jdata = {"persons":plist}

with open("persons_data.json", 'w') as pd:
    json.dump(jdata, pd)
pd.close()

with open("persons_data.json", 'r') as pd:
    jdt = json.load(pd)

print(json.dumps(jdt, indent=4))
import sqlite3 as sql
import json
from pprint import pprint as pprint

def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    return tables


def export_table_to_json(table_name):

    # get column names from the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    # col[1] is the column name
    columns = [col[1] for col in cursor.fetchall()]  

    # fetch all data from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # table data as list containing dictionaries of each row
    table_data = []
    for row in rows:
        row_dict = {columns[i]: row[i] for i in range(len(columns))}
        table_data.append(row_dict)
    #pprint(table_data)

    # wrap table data with table name
    table_dict = {table_name: table_data}

    # dump to json
    with open(f"{table_name}.json", "w") as f:
        json.dump(table_dict, f, indent=4)

    print(f"Exported {table_name} to {table_name}.json")


#main program
with sql.connect("Galactic_Imports.db") as conn:
    cursor = conn.cursor()

table_names = get_table_names(conn)

for table in table_names:
    export_table_to_json(table)

conn.close()
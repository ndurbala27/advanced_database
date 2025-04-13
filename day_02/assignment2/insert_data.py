from pprint import pprint as pprint
import sqlite3

global CURR

db_file = "acme.db"  # Change to your actual DB path
connection = sqlite3.connect(db_file)
CURR = connection.cursor()
print(f"Connected to {db_file} . . .")


def get_tables() -> dict:
    """collect table names and their columns and type from acme database"""

    CURR.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    tables = CURR.fetchall()
    tbl_names = []
    tbl_cols = []

    for table in tables:
        name, columns = table
        first_paren = columns.find("(")+1
        last_paren = columns.rfind(")")
        tbl_names.append(name)
        tbl_cols.append(columns[first_paren:last_paren].split(","))

    #clean colums
    clean_cols = []
    for i in range(len(tbl_cols)):
        col_set = [col.strip() for col in tbl_cols[i]]
        for c in col_set:
            if "\t" in c:
                cc = [c.replace("\t", "").replace('"', " ").strip() for c in col_set]
            else:
                cc = [c.replace('"', "").strip() for c in col_set]
        
        clean_cols.append(cc)

    tbl_dict = {}
    for i, tbl in enumerate(tbl_names):
        tbl_dict[tbl] = clean_cols[i]

    return tbl_dict


def select_table_name():
    db = get_tables()

    while True:
        print(f"{'TABLES':-^26}")
        for table in db.keys():
            print(table)
        # Prompt the user to select a table name
        table_name = input("\nEnter table name from list above: ")
        try:
            return table_name, db[table_name.lower()]
        except KeyError:
            print("\nTable does not exist!")
            continue



def input_data(columns) -> list:
    data_types = []
    values = []
    for col in columns:
        data_types.append(col[col.find(" ")+1:])

    for i, col in enumerate(columns):
        if data_types[i] == 'INTEGER':
            try:
                values.append(int(input(f"\nColumn: '{col[:col.find(" ")]}'\nData type:{col[col.find(" "):]}\t\tEnter a value: ")))
            except ValueError:
                print("Must be an integer.")
        elif data_types[i] == 'REAL':
            try:
                values.append(float(input(f"\nColumn: '{col[:col.find(" ")]}'\nData type:{col[col.find(" "):]}\t\tEnter a value: ")))
            except ValueError:
                print("Must be a float.")
        elif data_types[i] == 'TEXT':
            str_val = input(f"\nColumn: '{col[:col.find(" ")]}'\nData type:{col[col.find(" "):]}\t\tEnter a value: ")
            values.append(f"'{str_val}'")

    return values



def build_insert_sql(values) -> str:
    # build 'insert into values' sql statement
    insert_str = f"INSERT INTO {table} VALUES("
    for value in values:
        col_val = f'{value},'
        insert_str += col_val

    # clean up sql statement, remove last comma from previous process
    insert_str = f"{insert_str[:insert_str.rfind(",")]});"

    return insert_str



#main program
while True:
    table, columns = select_table_name()
    print(f"Let's insert data into: {table}")
    
    values = input_data(columns)
    
    insert_str = build_insert_sql(values)

    CURR.execute(insert_str)

    connection.commit()
    while True:
        again = input("Create another record? [y or n]")
        match again:
            case 'y':
                break
            case 'n':
                print("Goodbeye")
                CURR.close()
                connection.close()
                exit(0)
            case _:
                print("y or n")
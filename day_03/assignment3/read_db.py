import sqlite3


db_file = "acme.db"  # Change to your actual DB path
connection = sqlite3.connect(db_file)
curr = connection.cursor()
print(f"\nConnected to {db_file} . . .")


def query_database():
    """output list of tables from database for user to select"""
    curr.execute("SELECT name FROM sqlite_master WHERE type='table';")
    querry = curr.fetchall()

    print(f"\n{'TABLES':-^26}")
    for table in querry:
        print(table[0])


def query_table(name):
    """query table selected by user, and convert all data points (dp) to string,
     and return column names and data set for output"""
    
    curr.execute(f"SELECT * FROM {name};")
    table_set = curr.fetchall()

    curr.execute(f"PRAGMA table_info({name});")
    column_row = curr.fetchall()

    column_names = []
    for column in column_row:
        column_names.append(column[1])

    data_set = []
    for row_set in table_set:
        row_data = []
        for dp in row_set:
            if type(dp) is int:
                row_data.append((str(dp)))
            elif type(dp) is float:
                row_data.append(f"{dp:.2f}")
            else:
                row_data.append(dp)
        data_set.append(row_data)
    
    return column_names, data_set


def ouput_table_data(name):
    """Display the information from the chosen table 
    in a user-friendly manner (not just the tuple)"""
    columns, data_set = query_table(name)

    print(f"\nTable: {name.title()}")

    column_header = "".join([f"{column.upper():<20}" for column in columns])
    print(column_header)
    print("-"*len(column_header))

    for row in data_set:
        print("".join([f"{value.title():<20}" for value in row]))


# main program
while True:
    # present the list of tables in the database
    query_database()

    # Prompt the user to select a table name
    print(f"\n(enter 'q' to quit)")
    table_name = input("\nEnter table name from list above: ").lower()
    if table_name == 'q':
        exit(0)

    try:
        ouput_table_data(table_name)
        ans = input("\nWould you like to view another table? (enter 'y' or 'n'): ")
        match ans:
            case 'y':
                continue
            case _:
                print("Goodbye!")
                exit(0)
    except sqlite3.OperationalError:
        print(f"\nNo such table: {table_name}")
        continue
import sqlite3

def create_table(name: str, schema: dict) -> bool:
    # Create a connection to a database.
    conn = sqlite3.connect('acme.db')
    curr = conn.cursor()

    # build create table sql statement
    sql_str = f'CREATE TABLE "{name}"('
    for col, type in schema.items():
        col_type = f'\n\t"{col}" {type},'
        sql_str += col_type

    # clean up sql statement, remove last comma from previous process
    sql_str = f"{sql_str[:sql_str.rfind(",")]})"

    # provide user an opportunity for final review and verify to commit sql statement
    print(f"\nReady to execute the following sql statement:\n{sql_str}")
    response = input(f"Type and enter 'yes' or 'no': ")
    match response:
        case 'yes':
            curr.execute(sql_str)
            conn.commit()
            print("Table created!")
            curr.close()
            conn.close()
            return True
        case 'no':
            return False
        case _:
            return False


def data_type() -> str:
    type = ['TEXT', 'INTEGER', 'REAL', 'BLOB', 'NUMERIC']
    
    while True:
        print(f"Select from the following data types.")
        for n, t in enumerate(type, 1):
            print(f"{t:>7} = {n}")

        try:
            selected=int(input("Enter associated number: "))-1
            if selected < 5:
                return type[selected]
            else:
                print("\nYou didn't select 1, 2, 3, 4, or 5.")
                continue
        except ValueError:
            print("\nERROR: Must enter a number!")
            return None


def add_column():
    while True:
        another_col = input("\nAdd another column? [y or n]: ")        
        match another_col:
            case 'y':
                return True
            case 'n':
                return False
            case _:
                print("y or n?")


def add_table():
    while True:
        another_tbl = input("\nAdd another table? [y or n]: ")
        match another_tbl:
            case 'y':
                return True
            case 'n':
                return False
            case _:
                print("y or n?")


def quit(ans):
    if ans == 'y':
        print("Goodbeye")
        exit(0)
    else:
        return False


# start main program
while True:
    # clear table schema (dictionary)
    tbl_schema = {}
    print("Let's create a new table.")
    # prompt user for table name
    tbl_name = input("Table Name: ")
    
    # prompt user for column(s)
    while True:
        column = input("Column name: ")
        #select a data type
        type = data_type()
        if type:
            tbl_schema[column] = type
            # is it true, the user wants to add another column?
            if add_column():
                # circle back to 'Column name: ' prompt
                continue
            else:
                break
    
    # verify table was created successfully in database
    if create_table(tbl_name, tbl_schema):
         # is it true, the user wants to add another table?
        if add_table():
            # circle back to the start of the main program
            continue
        else:
            print("Goodbeye")
            exit(0)
    elif create_table(tbl_name, tbl_schema) == False:
        print("Nothing was committed to the database.")
        ans = input("Do you want to quit? [y or n]: ")
        if not quit(ans):
            continue
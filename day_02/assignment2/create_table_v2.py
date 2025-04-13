import sqlite3

DATA_TYPES = ['TEXT', 'INTEGER', 'REAL', 'BLOB', 'NUMERIC']

def get_data_type() -> str:
    while True:
        print("Select a data type:")
        for idx, dtype in enumerate(DATA_TYPES, 1):
            print(f"{idx}. {dtype}")
        try:
            selected = int(input("Enter number (1-5): ")) - 1
            if 0 <= selected < len(DATA_TYPES):
                return DATA_TYPES[selected]
            else:
                print("Invalid selection. Choose a number between 1 and 5.")
        except ValueError:
            print("ERROR: Must enter a number!")

def yes_or_no(prompt: str) -> bool:
    while True:
        ans = input(f"{prompt} [y or n]: ").strip().lower()
        if ans in ('y', 'n'):
            return ans == 'y'
        print("Please enter 'y' or 'n'.")

def create_table(name: str, schema: dict) -> bool:
    conn = sqlite3.connect('acme.db')
    cursor = conn.cursor()

    columns = [f'"{col}" {dtype}' for col, dtype in schema.items()]
    sql = f'CREATE TABLE "{name}" (\n    ' + ',\n    '.join(columns) + '\n);'

    print("\nReady to execute the following SQL statement:\n")
    print(sql)
    if input("Type 'yes' to confirm: ").strip().lower() == 'yes':
        try:
            cursor.execute(sql)
            conn.commit()
            print("✅ Table created successfully!")
            return True
        except sqlite3.Error as e:
            print(f"❌ SQLite error: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("❌ Table creation cancelled.")
        cursor.close()
        conn.close()
        return False

def define_schema() -> dict:
    schema = {}
    while True:
        col_name = input("Column name: ").strip()
        data_type = get_data_type()
        if data_type:
            schema[col_name] = data_type
            if not yes_or_no("Add another column?"):
                break
    return schema

def main():
    print("Welcome to ACME Table Creator!\n")
    while True:
        table_name = input("Enter table name: ").strip()
        table_schema = define_schema()
        
        if create_table(table_name, table_schema):
            if not yes_or_no("\nCreate another table?"):
                print("Goodbye 👋")
                break
        else:
            if not yes_or_no("\nDo you want to try again?"):
                print("Goodbye 👋")
                break

if __name__ == "__main__":
    main()

import sqlite3

DATA_TYPES = ['TEXT', 'INTEGER', 'REAL', 'BLOB', 'NUMERIC']
DB_FILE = "acme.db"

def connect_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    print(f"Connected to {DB_FILE}")
    return conn

def get_table_schemas(conn) -> dict:
    """Return a dictionary: {table_name: [(column_name, type), ...]}"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    schemas = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        schema = [(row[1], row[2]) for row in cursor.fetchall()]
        schemas[table] = schema

    return schemas

def select_table(schemas: dict) -> tuple:
    """Prompt user to select a valid table from schema dict"""
    while True:
        print(f"\n{' AVAILABLE TABLES ':=^40}")
        for table in schemas:
            print(f"- {table}")
        choice = input("Enter table name: ").strip()
        if choice in schemas:
            return choice, schemas[choice]
        print("Invalid table. Try again.")

def prompt_value(col_name: str, col_type: str):
    while True:
        val = input(f"Column: {col_name} ({col_type})\nEnter a value: ")
        try:
            if col_type == 'INTEGER':
                return int(val)
            elif col_type == 'REAL':
                return float(val)
            elif col_type == 'TEXT':
                return str(val)
            elif col_type in ('BLOB', 'NUMERIC'):
                return val  # Just pass raw
            else:
                print("Unsupported data type.")
                return None
        except ValueError:
            print(f"Invalid input for {col_type}. Try again.")

def collect_row_data(schema: list) -> list:
    """Collect one row's worth of values matching schema."""
    values = []
    for col_name, col_type in schema:
        val = prompt_value(col_name, col_type)
        values.append(val)
    return values

def insert_row(conn, table: str, values: list):
    placeholders = ", ".join(["?"] * len(values))
    sql = f"INSERT INTO {table} VALUES ({placeholders})"
    try:
        conn.execute(sql, values)
        conn.commit()
        print("✅ Record inserted successfully.\n")
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")

def yes_or_no(prompt: str) -> bool:
    while True:
        ans = input(f"{prompt} [y/n]: ").strip().lower()
        if ans in ('y', 'n'):
            return ans == 'y'
        print("Please enter 'y' or 'n'.")

def main():
    conn = connect_db()
    schemas = get_table_schemas(conn)

    while True:
        table, schema = select_table(schemas)
        print(f"\nInserting data into '{table}'")

        row_data = collect_row_data(schema)
        insert_row(conn, table, row_data)

        if not yes_or_no("Insert another record?"):
            print("Goodbye 👋")
            break

    conn.close()

if __name__ == "__main__":
    main()

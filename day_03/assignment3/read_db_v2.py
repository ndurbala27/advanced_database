import sqlite3

def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]

def get_column_names(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [col[1] for col in cursor.fetchall()]

def fetch_all_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()

def display_table_data(headers, rows):
    col_widths = [max(len(str(h)), *(len(str(row[i])) for row in rows)) for i, h in enumerate(headers)]

    # Print header
    header_row = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))

    # Print rows
    for row in rows:
        print(" | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row)))

def main():
    conn = sqlite3.connect("acme.db")

    table_names = get_table_names(conn)
    if not table_names:
        print("No tables found in the database.")
        return

    while True:
        print("\nAvailable Tables:")
        for i, name in enumerate(table_names, 1):
            print(f"{i}. {name}")

        choice = input("Enter the table name to view: ").strip()

        if choice not in table_names:
            print(f"Error: '{choice}' is not a valid table name.")
            continue

        headers = get_column_names(conn, choice)
        rows = fetch_all_data(conn, choice)

        print(f"\nContents of table '{choice}':\n")
        if not rows:
            print("Table is empty.")
        else:
            display_table_data(headers, rows)

        again = input("\nWould you like to view another table? (y/n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            break

    conn.close()

if __name__ == "__main__":
    main()

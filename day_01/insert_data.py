import sqlite3 as sql

conn = sql.connect('people.db')
curr = conn.cursor()


while True:
    print("Insert a new record")
    name = input("Name: ")
    try:
        age = int(input("Age: "))
    except ValueError:
        print("number's only for age")
    
    city = input("City: ")

    curr.execute(
        f"""INSERT INTO persons VALUES(
                "{name.lower()}",
                {age},
                "{city.lower()}")"""
    )

    conn.commit()
    while True:
        again = input("Create another record? [y or n]")
        match again:
            case 'y':
                break
            case 'n':
                print("Goodbeye")
                curr.close()
                conn.close()
                exit(0)
            case _:
                print("y or n")
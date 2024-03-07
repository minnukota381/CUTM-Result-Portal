import sqlite3

def list_tables():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    cur.close()
    conn.close()

    return tables

def delete_table(table_name):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cur.fetchone()
    if result is None:
        print(f"The table \"{table_name}\" does not exist.")
    else:
        drop_table_query = f"DROP TABLE IF EXISTS \"{table_name}\";"
        cur.execute(drop_table_query)
        conn.commit()
        print(f"Table \"{table_name}\" successfully deleted from the database.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    tables = list_tables()
    print("Tables in the database:")
    for index, table in enumerate(tables, start=1):
        print(f"{index}. {table[0]}")

    if tables:
        table_index = int(input("Enter the number corresponding to the table you want to delete: "))
        if 1 <= table_index <= len(tables):
            table_name = tables[table_index - 1][0]
            delete_table(table_name)
        else:
            print("Invalid table number. Please enter a valid table number.")
    else:
        print("There are no tables in the database.")

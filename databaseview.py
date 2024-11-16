import sqlite3
import os

# Make sure to specify the correct path to the database
db_path = os.path.join(os.getcwd(), 'instance/site.db')  # Or 'instance/site.db' if it's in the instance folder

# Connect to the SQLite database
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        print("No tables found in the database.")
    else:
        # Loop through the tables and display their contents
        for table_name in tables:
            print(f"\nTable: {table_name[0]}")
            cursor.execute(f"PRAGMA table_info({table_name[0]});")
            columns = cursor.fetchall()
            print(f"Columns: {[col[1] for col in columns]}")

            cursor.execute(f"SELECT * FROM {table_name[0]};")
            rows = cursor.fetchall()

            if not rows:
                print("No data found in this table.")
            else:
                for row in rows:
                    print(row)

    # Close the connection to the database
    conn.close()

except sqlite3.OperationalError as e:
    print(f"OperationalError: {e}")

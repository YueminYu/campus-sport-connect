import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/site.db')  # Update with your actual path
cursor = conn.cursor()

# Delete the alembic version
cursor.execute("DELETE FROM alembic_version;")
conn.commit()

print("Alembic version removed successfully.")

# Close the connection to the database
conn.close()

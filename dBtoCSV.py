
import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Execute a query to fetch data from the 'CUTM' table
cursor.execute("SELECT * FROM CUTM")

# Fetch all rows from the result set
rows = cursor.fetchall()

# Specify the filename for the CSV file
csv_filename = 'cutm_data.csv'

# Write the fetched data to a CSV file
with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header row based on the column names
    csv_writer.writerow([i[0] for i in cursor.description])
    
    # Write the data rows
    csv_writer.writerows(rows)

# Close the database connection
conn.close()

print(f"Data has been exported to {csv_filename}")

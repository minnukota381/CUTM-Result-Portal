
import sqlite3
import csv

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM CUTM")

rows = cursor.fetchall()

csv_filename = 'cutm_data.csv'

with open(csv_filename, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    csv_writer.writerow([i[0] for i in cursor.description])
    
    csv_writer.writerows(rows)

conn.close()

print(f"Data has been exported to {csv_filename}")

import pandas as pd
import sqlite3
import os

directory = 'results'
conn = sqlite3.connect('database.db')

dfs = []

for filename in os.listdir(directory):
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        file_path = os.path.join(directory, filename)
        
        xl = pd.ExcelFile(file_path)
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name)
            dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_sql('CUTM', conn, if_exists='replace', index=False)

conn.close()

print("Excel files successfully combined and converted to a single SQLite table.")
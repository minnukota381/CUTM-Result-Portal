import pandas as pd
import sqlite3
import os

directory = "results"
db_name = "database.db"
table_name = "CUTM"

conn = sqlite3.connect(db_name)

dfs = []

for filename in os.listdir(directory):
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        file_path = os.path.join(directory, filename)

        print(f"✅ Reading file: {filename}")

        # choose engine based on file extension
        engine = "openpyxl" if filename.endswith(".xlsx") else "xlrd"

        try:
            xl = pd.ExcelFile(file_path, engine=engine)

            for sheet_name in xl.sheet_names:
                print(f"   ➜ Sheet: {sheet_name}")

                df = pd.read_excel(xl, sheet_name=sheet_name, engine=engine)

                # optional: add source info
                df["source_file"] = filename
                df["source_sheet"] = sheet_name

                dfs.append(df)

        except Exception as e:
            print(f"❌ Skipping file due to error: {filename}")
            print("   Error:", e)
            continue

# If no data found
if len(dfs) == 0:
    print("⚠️ No Excel data found to insert into database.")
    conn.close()
    exit()

combined_df = pd.concat(dfs, ignore_index=True)

# save into sqlite
combined_df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.close()

print("\n✅ Done! All Excel data saved into SQLite database successfully.")
print(f"📌 Database: {db_name}")
print(f"📌 Table: {table_name}")
print(f"📌 Total rows inserted: {len(combined_df)}")

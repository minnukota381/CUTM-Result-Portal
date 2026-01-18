import pandas as pd
import sqlite3
import os

directory = "results"
db_name = "database.db"
table_name = "CUTM"

def fix_reg_no(value):
    """
    Fix Reg_No values like:
    230101110016.0  -> 230101110016
    2.30101E+11     -> 230101000000 (converted properly)
    """
    if pd.isna(value):
        return ""

    x = str(value).strip()

    # scientific notation like 2.30101E+11
    if "E+" in x or "e+" in x:
        try:
            return str(int(float(x)))
        except:
            return x

    # remove .0
    if x.endswith(".0"):
        x = x[:-2]

    return x.strip()

# ✅ Connect to SQLite
conn = sqlite3.connect(db_name)

dfs = []

for filename in os.listdir(directory):
    if filename.endswith(".xlsx") or filename.endswith(".xls"):
        file_path = os.path.join(directory, filename)
        ext = os.path.splitext(filename)[1].lower()

        try:
            # ✅ Select engine based on extension
            if ext == ".xlsx":
                engine = "openpyxl"
            elif ext == ".xls":
                engine = "xlrd"
            else:
                continue

            print(f"\n📄 Reading file: {filename}  (engine={engine})")

            xl = pd.ExcelFile(file_path, engine=engine)

            for sheet_name in xl.sheet_names:
                try:
                    df = pd.read_excel(xl, sheet_name=sheet_name)

                    # ✅ Fix Reg_No column
                    if "Reg_No" in df.columns:
                        df["Reg_No"] = df["Reg_No"].apply(fix_reg_no)

                    # ✅ Clean Sem & Name
                    if "Sem" in df.columns:
                        df["Sem"] = df["Sem"].astype(str).str.strip()

                    if "Name" in df.columns:
                        df["Name"] = df["Name"].astype(str).str.strip()

                    df["source_file"] = filename
                    df["source_sheet"] = sheet_name

                    dfs.append(df)
                    print(f"✅ Loaded sheet: {sheet_name}  Rows: {df.shape[0]}  Cols: {df.shape[1]}")

                except Exception as e:
                    print(f"❌ Error reading sheet '{sheet_name}' in {filename}: {e}")

        except Exception as e:
            print(f"❌ Error reading file {filename}: {e}")

# ✅ Combine and insert into SQLite
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)

    combined_df.to_sql(table_name, conn, if_exists="replace", index=False)

    print("\n✅ Excel files successfully combined and stored into SQLite table:", table_name)
    print("📌 Total rows inserted:", combined_df.shape[0])
else:
    print("\n⚠️ No valid Excel data found to insert.")

conn.close()

import os
import win32com.client as win32

folder = "results"

excel = win32.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

for filename in os.listdir(folder):
    if filename.lower().endswith(".xlsx"):
        path = os.path.abspath(os.path.join(folder, filename))
        print("Repairing:", filename)

        try:
            wb = excel.Workbooks.Open(path)
            wb.Save()
            wb.Close(False)
            print("✅ Re-saved:", filename)
        except Exception as e:
            print("❌ Failed:", filename)
            print("   Error:", e)

excel.Quit()
print("✅ Repair finished")

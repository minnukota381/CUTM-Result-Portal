import os
import win32com.client as win32

folder = "results"

excel = win32.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

for filename in os.listdir(folder):
    if filename.lower().endswith(".xls") and not filename.lower().endswith(".xlsx"):
        xls_path = os.path.abspath(os.path.join(folder, filename))
        xlsx_path = os.path.abspath(os.path.join(folder, filename + "x"))  # adds x -> .xlsx

        print("Converting:", filename)

        wb = excel.Workbooks.Open(xls_path)
        wb.SaveAs(xlsx_path, FileFormat=51)  # 51 = xlOpenXMLWorkbook (.xlsx)
        wb.Close(False)

excel.Quit()
print("✅ All .xls converted to .xlsx")

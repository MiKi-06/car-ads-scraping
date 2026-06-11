from openpyxl import Workbook

class Excelexporter():
  def __init__(self):
    try:
      self.wb = Workbook()
      self.sheet = self.wb.active
      self.sheet.title = 'CAR ads Data'
      self.sheet["A1"] = "Title"
      self.sheet["B1"] = "Condition"
      self.sheet["C1"] = "Price"
      self.sheet["D1"] = "Link"
      self.sheet["E1"] = "Source"
    except Exception as e:
      print(e)

  def excel_submit_records(self, i, title, link, price, milage, date, source):
    self.sheet[f"A{i+2}"] = title
    self.sheet[f"B{i+2}"] = milage
    self.sheet[f"C{i+2}"] = price
    self.sheet[f"D{i+2}"] = link
    self.sheet[f"E{i+2}"] = date
    self.sheet[f"F{i+2}"] = source

  def close(self):
    self.wb.save(r".\\output\\ads.xlsx")
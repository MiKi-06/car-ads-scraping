import sqlite3
from openpyxl import Workbook
class Database():
  def __init__(self):
    try:
      with sqlite3.connect(r".\\output\\bama_scraping.db") as conn:
        self.cursor = conn.cursor()
        self.make_table()
        self.connect = conn
    except sqlite3.OperationalError as e:
      print(e)
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
  def make_table(self):
    # Table init
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS ads (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      milage INTEGER,
                      price INTEGER,
                      link TEXT UNIQUE,
                      date TEXT,
                      source TEXT);""")

  def avg_by_models(self):
    pass
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS avg_price_by_models(
                        model TEXT PRIMARY KEY,
                        avg_price REAL
                        );""")
    self.cursor.execute("""INSERT OR REPLACE INTO avg_price_by_models(
                        model, avg_price)
                        SELECT title, AVG((price))
                        FROM ads
                        WHERE price IS NOT NULL
                        GROUP BY title;""")
    self.connect.commit()

  def sqlite_submit_records(self, title, link, price, milage, date, source):
    try:
      # Record insertion
      self.cursor.execute("""INSERT OR IGNORE INTO ads(title, milage, price, link, date, source)
                              VALUES(?, ?, ?, ?, ?, ?);""", (title, milage, price, link, date, source))
      
    except sqlite3.OperationalError as e:
      print(e)

  def sqlite_save(self):
    self.connect.commit()

  def excel_submit_records(self, i, title, link, price, milage, date, source):
    self.sheet[f"A{i+2}"] = title
    self.sheet[f"B{i+2}"] = milage
    self.sheet[f"C{i+2}"] = price
    self.sheet[f"D{i+2}"] = link
    self.sheet[f"E{i+2}"] = date
    self.sheet[f"F{i+2}"] = source

  def excel_save(self):
    self.wb.save(r".\\output\\ads.xlsx")
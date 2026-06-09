import sqlite3

class Database():
  def __init__(self):
    try:
      with sqlite3.connect(r".\\output\\bama_scraping.db") as conn:
        self.cursor = conn.cursor()
        self.make_table()
    except sqlite3.OperationalError as e:
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


  def sqlite_submit_records(self, title, link, price, milage, date, source):
    try:
      # Record insertion
      self.cursor.execute("""INSERT OR IGNORE INTO ads(title, milage, price, link, date, source)
                              VALUES(?, ?, ?, ?, ?, ?);""", (title, milage, price, link, date, "bama"))
      
    except sqlite3.OperationalError as e:
      print(e)

  def excel_submit_records():
    pass
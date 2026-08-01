import sqlite3
from datetime import datetime
class Database():
  def __init__(self):
    try:
      self.conn = sqlite3.connect(r".\\output\\bama_scraping.db")
      self.conn.row_factory = sqlite3.Row
      self.cursor = self.conn.cursor()
      self.create_tables()
    except sqlite3.OperationalError as e:
      print(e)

  # Creates the main table (ads)
  def create_tables(self):
    # Table init
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS ads (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      model TEXT NOT NULL,
                      year INT,
                      milage INTEGER,
                      price INTEGER,
                      link TEXT UNIQUE,
                      date TEXT,
                      source TEXT);""")
    
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS model_cache (
                      model TEXT PRIMARY KEY,
                      ads_count INTEGER NOT NULL,
                      last_update TEXT NOT NULL
                  );""")

    self.cursor.execute("""CREATE TABLE IF NOT EXISTS metadata(
                        key text PRIMARY KEY,
                        value TEXT);""")

  def update_last_update(self, date=None):
    if date is None:
      date = datetime.now().isoformat()

    self.cursor.execute("""INSERT OR REPLACE INTO metadata(key, value)
                        VALUES ('last_update', ?)""", (date,))

  def get_last_update(self):
    self.cursor.execute("""SELECT value
                        FROM metadata
                        WHERE key = 'last_update';""")
    row = self.cursor.fetchone()
    if row:
      return row[0]
    else:
      return None
  # Returns all the car models
  def fetch_models(self):
    self.cursor.execute("""SELECT model FROM ads
                          GROUP BY model;
                          """)
    rows = self.cursor.fetchall()
    models = [row['model'] for row in rows]
    if models is None:
      return None
    return models

  # Returns not-zero priced ads related to the given car model
  def fetch_ads(self, model="رنو، تندر 90"):
    self.cursor.execute("""SELECT * FROM ads
                        WHERE model = ? AND price IS NOT NULL""", (model,))
    
    rows = self.cursor.fetchall()
    if not rows:
      return []
    return [dict(row) for row in rows]
  
  # Gets not-zero prices for each car model
  def get_prices(self, model= "رنو، تندر 90"):
    self.cursor.execute("""SELECT price FROM ads
                        WHERE model = ? AND price IS NOT NULL""", (model,))
    rows = self.cursor.fetchall()
    if not rows:
      return []
    prices = [row["price"] for row in rows if row["price"] is not None]
    return prices

  # Inserts ad into ads table
  def sqlite_submit_record(self, ad):
    try:
      # Record insertion
      self.cursor.execute("""INSERT OR REPLACE INTO ads(model, year, milage, price, link, date, source)
                            VALUES(?, ?, ?, ?, ?, ?, ?);""",
                            (ad.model, ad.year, ad.milage, ad.price, ad.link, ad.date, ad.source))
      self.conn.commit()
    except sqlite3.OperationalError as e:
      print(e)
    except Exception as e:
      print(f"database.py sqlite_sumbit_record():{e}")


  def insert_into(self, table, values):
    self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      score TEXT,
                      diff_percent REAL,
                      model TEXT NOT NULL,
                      year INT,
                      milage INTEGER,
                      price INTEGER,
                      link TEXT UNIQUE,
                      date TEXT,
                      source TEXT);""")
    for value in values:
      try:
        self.cursor.execute(
                          f"""
                          INSERT OR REPLACE INTO {table}
                          (score, diff_percent, model, year, milage, price, link, date, source)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                          """,
                          (   
                              value["score"],
                              value["diff_percent"],
                              value["model"],
                              value["year"],
                              value["milage"],
                              value["price"],
                              value["link"],
                              value["date"],
                              value["source"]
                          ),
                        )
      except sqlite3.OperationalError as e:
        print(e)

  def get_ad_by_url(self, url):
    self.cursor.execute("""SELECT * FROM ads
                        WHERE link = ?""", (url,))
    row = self.cursor.fetchone()
    if row:
      return dict(row)
    else:
      return None

  # Saves database changes and closes the connection
  def close(self):
    self.conn.commit()
    self.conn.close()

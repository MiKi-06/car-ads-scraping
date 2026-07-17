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
    
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS metadata(
                        key text PRIMARY KEY,
                        value TEXT);""")

  def update_last_update(self, date=None):
    if date is None:
      date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    self.cursor.execute("""INSERT OR REPLACE INTO metadata(key, value)
                        VALUES ('last_update', ?)""", (date,))

  def get_last_update(self):
    self.cursor.execute("""SELECT value
                        FROM metadata
                        WHERE key = 'last_update';""")
    return self.cursor.fetchone()[0]

  # Returns all the car models
  def fetch_models(self):
    self.cursor.execute("""SELECT model FROM ads
                          GROUP BY model;
                          """)
    rows = self.cursor.fetchall()
    models = [row['model'] for row in rows]
    return models

  # Calculates avg price for every model and stores them in new table
  def avg_of_models(self):
    
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS avg_price_of_models(
                        model TEXT PRIMARY KEY,
                        avg_price REAL,
                        link TEXT
                        );""")
    self.cursor.execute("""INSERT OR REPLACE INTO avg_price_by_models(
                        model, avg_price)
                        SELECT model, AVG((price))
                        FROM ads
                        WHERE price IS NOT NULL
                        GROUP BY model;""")
    self.conn.commit()

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
  
  # Finds the top expensive ad for each model and stores in new table
  def highest_price_by_models(self):
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS highest_price_by_models(
                        model TEXT PRIMARY KEY,
                        highest_price REAL,
                        link TEXT
                        );""")
    self.cursor.execute("""INSERT OR REPLACE INTO highest_price_by_models(
                        model, highest_price, link)
                        SELECT model, MAX((price)), link
                        FROM ads
                        GROUP BY model
                        ORDER by price DESC;""")
    self.conn.commit()

  # Finds the cheapest ad for each model and stores in new table
  def lowest_price_by_models(self):
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS lowest_price_by_models(
                        model TEXT PRIMARY KEY,
                        lowest_price REAL,
                        link TEXT
                        );""")
    self.cursor.execute("""INSERT OR REPLACE INTO lowest_price_by_models(
                        model, lowest_price, link)
                        SELECT model, MIN((price)), link
                        FROM ads
                        GROUP BY model
                        ORDER by price ASC;""")
    self.conn.commit()

  # Finds top 5 expensive ad for each model and stores in new table
  def expensive_cars(self):
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS expensive_cars(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        model TEXT,
                        price REAL,
                        link TEXT
                        );""")
    self.cursor.execute("""DELETE FROM expensive_cars;""")
    self.cursor.execute("""INSERT INTO expensive_cars(model, price, link)
                        SELECT model, price, link
                        FROM ads
                        WHERE price IS NOT NULL
                        ORDER BY price DESC
                        LIMIT 5;""")
    self.conn.commit()
  
  # Finds top 5 cheap ad for each model and stores in new table
  def cheapest_cars(self):
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS cheapest_cars (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        model TEXT,
                        price REAL,
                        link TEXT);""")
    self.cursor.execute("""DELETE FROM cheapest_cars;""")
    self.cursor.execute("""INSERT INTO cheapest_cars(
                        model, price, link)
                        SELECT model, price, link
                        FROM ads
                        WHERE price IS NOT NULL
                        ORDER by price ASC
                        LIMIT 5;""")
    self.conn.commit()

  # Inserts ad into ads table
  def sqlite_submit_record(self, ad):
    try:
      # Record insertion
      self.cursor.execute("""INSERT OR IGNORE INTO ads(model, year, milage, price, link, date, source)
                            VALUES(?, ?, ?, ?, ?, ?, ?);""",
                            (ad.model, ad.year, ad.milage, ad.price, ad.link, ad.date, ad.source))
      self.conn.commit()
    except sqlite3.OperationalError as e:
      print(e)

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

  # Saves database changes and closes the connection
  def close(self):
    self.conn.commit()
    self.conn.close()

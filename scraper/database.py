import sqlite3
class Database():
  def __init__(self):
    try:
      self.conn = sqlite3.connect(r".\\output\\bama_scraping.db")
      self.cursor = self.conn.cursor()
      self.make_table()
      self.connect = self.conn
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

  def avg_by_models(self):
    
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS avg_price_by_models(
                        model TEXT PRIMARY KEY,
                        avg_price REAL,
                        link TEXT
                        );""")
    self.cursor.execute("""INSERT OR REPLACE INTO avg_price_by_models(
                        model, avg_price, link)
                        SELECT title, AVG((price)), link
                        FROM ads
                        WHERE price IS NOT NULL
                        GROUP BY title;""")
    self.connect.commit()

  def get_prices(self, model= "رنو، تندر 90"):
    self.cursor.execute("""SELECT price FROM ads
                        WHERE title = ? AND price IS NOT NULL""", (model,))
    rows = self.cursor.fetchall()
    if not rows:
      return None
    prices = [row[0] for row in rows if rows[0] is not None]
    return prices
  
  def highest_price_by_models(self):
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS highest_price_by_models(
                        model TEXT PRIMARY KEY,
                        highest_price REAL,
                        link TEXT
                        );""")
    self.cursor.execute("""INSERT OR REPLACE INTO highest_price_by_models(
                        model, highest_price, link)
                        SELECT title, MAX((price)), link
                        FROM ads
                        GROUP BY title
                        ORDER by price DESC;""")
    self.connect.commit()

  def lowest_price_by_models(self):
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS lowest_price_by_models(
                        model TEXT PRIMARY KEY,
                        lowest_price REAL,
                        link TEXT
                        );""")
    self.cursor.execute("""INSERT OR REPLACE INTO lowest_price_by_models(
                        model, lowest_price, link)
                        SELECT title, MIN((price)), link
                        FROM ads
                        GROUP BY title
                        ORDER by price ASC;""")
    self.connect.commit()

  def expensive_cars(self):
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS expensive_cars(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        model TEXT,
                        price REAL,
                        link TEXT
                        );""")
    self.cursor.execute("""DELETE FROM expensive_cars;""")
    self.cursor.execute("""INSERT INTO expensive_cars(model, price, link)
                        SELECT title, price, link
                        FROM ads
                        WHERE price IS NOT NULL
                        ORDER BY price DESC
                        LIMIT 5;""")
    self.connect.commit()
    
  def cheapest_cars(self):
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS cheapest_cars (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        model TEXT,
                        price REAL,
                        link TEXT);""")
    self.cursor.execute("""DELETE FROM cheapest_cars;""")
    self.cursor.execute("""INSERT INTO cheapest_cars(
                        model, price, link)
                        SELECT title, price, link
                        FROM ads
                        WHERE price IS NOT NULL
                        ORDER by price ASC
                        LIMIT 5;""")
    self.connect.commit()

  def sqlite_submit_records(self, title, link, price, milage, date, source):
    try:
      # Record insertion
      self.cursor.execute("""INSERT OR IGNORE INTO ads(title, milage, price, link, date, source)
                              VALUES(?, ?, ?, ?, ?, ?);""", (title, milage, price, link, date, source))
      
    except sqlite3.OperationalError as e:
      print(e)

  def close(self):
    self.connect.commit()
    self.conn.close()

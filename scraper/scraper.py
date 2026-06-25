from .advertisement import Advertisement
from .database import Database
from analysis.analysis import Analyzer
from reporter.market_report import Reporter
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from . import utils

#URL = "https://bama.ir/car/all/fars-shiraz?installment=0&price=300000000,1500000000&body=passenger_car"
TITLE_SELECTOR = "div.inline-flex.mb-1 span.text-neutral-10"
PRICE_SELECTOR = 'p.flex.items-center.justify-end.gap-1'

class Scraper:
  def __init__(self, min_price, max_price, db, city="fars-shiraz"):
    if db is None:
      db = Database()
    self.db = db
    self.URL = self.get_url(min_price, max_price, city)

  def get_url(self, min, max, city):
    if min is None or max is None or city is None:
      return "https://bama.ir/car/all/fars-shiraz?installment=0&price=300000000,1500000000&body=passenger_car"
    return f"https://bama.ir/car/all/{city}?installment=0&price={min},{max}&body=passenger_car"


  def scroll_to_bottom(self, driver, pause_time=2, max_attempts = 5):
    last_height = driver.execute_script("return document.body.scrollHeight")
    attempt = 0
    while attempt < max_attempts:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      
      time.sleep(pause_time)

      new_height = driver.execute_script("return document.body.scrollHeight")
      if last_height == new_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        final_height = driver.execute_script("return document.body.scrollHeight")
        if final_height == new_height:
          return True
        
      attempt +=1
      last_height = new_height

  def scrape(self):
    try:
      driver = webdriver.Edge()
      driver.get(self.URL)
      time.sleep(2)
      self.scroll_to_bottom(driver= driver)
      # Gets ads containers
      articles = driver.find_elements(By.TAG_NAME, "article")
      # Connecting to database and accessing modules
      analyzer = Analyzer(self.db)
      reporter = Reporter(analyzer)
      # Finds and inserts ads information into xlsx and database
      for i, article in enumerate(articles):
        try:
          # Finds the elements
          model = article.find_element(By.CSS_SELECTOR, TITLE_SELECTOR).text
          link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
          price = article.find_element(By.CSS_SELECTOR, PRICE_SELECTOR).text
          milage = article.find_element(By.CSS_SELECTOR, "span[dir='ltr']").text
          price = utils.get_digit(price)
          milage = utils.get_digit(milage)
          spans = article.find_elements(By.TAG_NAME, "span")
          date = utils.date_finder(spans)

          # temp default value:
          source = "bama"

          ad = Advertisement(model, milage, price, link, date, source)

          self.db.sqlite_submit_record(ad)
          yield i + 1, len(articles)
          
        except Exception as e:
          print(f"Error in article {i}: {e}")
          continue
      time.sleep(1)
      
    finally:

      reporter.get_report()
      driver.quit()

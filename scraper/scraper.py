from .advertisement import Advertisement
from .database import Database
from analysis.analysis import Analyzer
from reporter.market_report import Reporter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from . import utils

#URL = "https://bama.ir/car/all/fars-shiraz?installment=0&price=300000000,1500000000&body=passenger_car"
TITLE_SELECTOR = "div.inline-flex.mb-1 span.text-neutral-10"
PRICE_SELECTOR = 'p.flex.items-center.justify-end.gap-1'

class Scraper:
  def __init__(self, db, min_price=0, max_price=0, city="fars-shiraz"):
    if db is None:
      db = Database()
    self.db = db
    self.URL = self.get_url(min_price, max_price, city)

  def get_url(self, min_price, max_price, city):
    if min_price is None or max_price is None or city is None:
      return "https://bama.ir/car/all/fars-shiraz"
    return f"https://bama.ir/car/all/{city}?installment=0&price={min_price},{max_price}&body=passenger_car"


  def scroll_to_bottom(self, driver, pause_time=2):
    LOAD_BTN_SELECTOR = "//button//span[text()='بیشتر']/.."
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      
      time.sleep(pause_time)

      new_height = driver.execute_script("return document.body.scrollHeight")
      if last_height == new_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
          load_btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, LOAD_BTN_SELECTOR)))
          driver.execute_script("arguments[0].scrollIntoView(true);", load_btn)
          load_btn.click()
          time.sleep(pause_time)

          new_height = driver.execute_script("return document.body.scrollHeight")
        
          if new_height == last_height:
            return True
          else:
            last_height = new_height
        except (NoSuchElementException, TimeoutException):
          print("nosuch, timeout")
          return True
        except Exception as e:
          print("Error clicking btn")
          return True

      else:
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
      # Finds and inserts ads information into xlsx and database
      for i, article in enumerate(articles):
        try:
          price = 0
          # Finds the elements
          model = article.find_element(By.CSS_SELECTOR, TITLE_SELECTOR).text
          link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
          price = article.find_elements(By.CSS_SELECTOR, PRICE_SELECTOR)
          milage = article.find_element(By.CSS_SELECTOR, "span[dir='ltr']").text
          year = int(link[-4:])
          if price:
            price = utils.get_digit(price[0].text)
          else:
            price = 0
          milage = utils.get_digit(milage)
          spans = article.find_elements(By.TAG_NAME, "span")
          date = utils.date_finder(spans)

          # temp default value:
          source = "bama"

          ad = Advertisement(model, year, milage, price, link, date, source)

          self.db.sqlite_submit_record(ad)
          yield i + 1, len(articles)
          
        except NoSuchElementException:
          price = 0
        except Exception as e:
          print(f"Error in article {i}: {e}")
          continue
      time.sleep(1)
      
    finally:
      try:
        self.db.update_last_update()
        reporter = Reporter(analyzer)
        if reporter:
          reporter.get_report()
      except Exception as e:
        print(f"Report error: {e}")
        
      driver.quit()

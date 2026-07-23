from .advertisement import Advertisement
from .database import Database
from analysis.analysis import Analyzer
from reporter.market_report import Reporter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


  def scroll_to_bottom(self, driver, pause_time=2, threshold=10):
    
    loads = 0

    LOAD_BTN_SELECTOR = "//button//span[text()='بیشتر']/.."
    last_height = driver.execute_script("return document.body.scrollHeight")
    while loads < threshold:
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
          loads += 1

      else:
        last_height = new_height

  def scrape(self):
    try:
      driver = webdriver.Edge()
      driver.get(self.URL)
      time.sleep(2)
      analyzer = Analyzer(self.db)
      # Finds and inserts ads information into xlsx and database
      ads = self.collect_ads(driver=driver)
      for i, ad in enumerate(ads):
        self.db.sqlite_submit_record(ad)
        yield i+1, len(ads)
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

  def single_ad_scrape(self, url):
    driver = webdriver.Edge()
    try:
      driver.get(url)
      time.sleep(2)

      container = driver.find_element(By.CSS_SELECTOR, "div.flex.flex-col.gap-6.items-start.self-stretch")

      model = driver.find_element(By.CSS_SELECTOR, "h1.inline-block.text-right.w-full.text-base.leading-6.font-semibold.max-w-full.truncate").text
      milage = driver.find_elements(By.CSS_SELECTOR, "span.inline-block.text-right.w-full.text-sm.leading-6.font-normal.max-w-max")
      year = int(url[-4:])
      date = driver.find_element(By.CSS_SELECTOR, "span.text-neutral-10 > span").text
      milage = utils.get_digit(milage[1].text)
      date = utils.get_date(date)
      try:
        price = container.find_element(By.CSS_SELECTOR, "span[dir='ltr']").text
        price = utils.get_digit(price)
      except NoSuchElementException:
        price = 0
    except NoSuchElementException as e:
      print(e)
    except Exception as e:
      print(e)
      return None
    else:
      ad = Advertisement(model, year, milage, price, url, date, "bama")
      self.db.sqlite_submit_record(ad)
    finally:
      driver.quit()

  def scrape_model(self, model):
    try:
      driver = webdriver.Edge()
      driver.get("https://bama.ir/")
      time.sleep(2)

      search_btn = driver.find_element(By.CSS_SELECTOR, "#__nuxt > div > main > div > section > button")
      search_btn.click()
      search_bar = driver.find_element(By.TAG_NAME, "input")
      search_bar.send_keys(model)
      time.sleep(2)

      btn = driver.find_element(By.CSS_SELECTOR, "#__nuxt > div > div.fixed.inset-0.bg-white.w-full.h-full.flex.flex-col.z-100 > div.w-full.flex.justify-center > div > div > div > div > a:nth-child(1) > button")
      btn.click()
      time.sleep(2)
      ads =  self.collect_ads(driver, 1)
    except Exception as e:
      print(e)
    finally:
      driver.quit()
      return ads

  def collect_ads(self, driver, threshold=10):

    ads = []

    self.scroll_to_bottom(driver=driver, threshold=threshold)

    articles = driver.find_elements(By.TAG_NAME, "article")
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
        ads.append(ad)

      except NoSuchElementException:
        price = 0
      except Exception as e:
        print(f"Error in article {i}: {e}")
        continue
    
    return ads
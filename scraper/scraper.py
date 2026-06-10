from database import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import utils

def scroll_to_bottom(driver, pause_time=2, max_attempts = 5):
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

URL = "https://bama.ir/car/all/fars-shiraz?installment=0&price=300000000,1500000000&body=passenger_car"
title_selector = "div.inline-flex.mb-1 span.text-neutral-10"
price_selector = 'p.flex.items-center.justify-end.gap-1'
try:
  driver = webdriver.Edge()
  driver.get(URL)
  time.sleep(2)
  scroll_to_bottom(driver= driver)
  # Gets ads containers
  articles = driver.find_elements(By.TAG_NAME, "article")
  # Connecting to database
  db = Database()
  # Finds and inserts ads information into xlsx and database
  for i, article in enumerate(articles):
    try:
      # Finds the elements
      title = article.find_element(By.CSS_SELECTOR, title_selector).text
      link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
      price = article.find_element(By.CSS_SELECTOR, price_selector).text
      milage = article.find_element(By.CSS_SELECTOR, "span[dir='ltr']").text
      price = utils.get_digit(price)
      milage = utils.get_digit(milage)

      spans = article.find_elements(By.TAG_NAME, "span")
      date = utils.date_finder(spans)

      db.sqlite_submit_records(title, link, price, milage, date, "bama")
      db.excel_submit_records(i, title, link, price, milage, date, "bama")
      db.avg_by_models()
      db.highest_price_by_models()
      db.lowest_price_by_models()
      db.expensive_cars()
      db.cheapest_cars()
    except Exception as e:
      print(f"Error in article {i}: {e}")
      continue
  time.sleep(1)
finally:
  db.excel_save()
  db.sqlite_save()
  driver.quit()

from database import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import re
from jdatetime import datetime, timedelta
import time

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

def get_digit(string_data):
  try:
    digit = int(re.sub(r"[^\d]", "", string_data))
    return digit
  except ValueError:
    return 0

def fa_to_en(text):
    return text.translate(str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹",
        "0123456789"
    ))

def get_date(date):
  date = fa_to_en(date.strip())
  now = datetime.now()
  try:
    date = datetime.strptime(date, "%Y/%m/%d")
    return date.strftime("%Y-%m-%d %H:%M:%S")
  except ValueError:
    if "لحظاتی پیش" in date:
      return now.strftime("%Y-%m-%d %H:%M:%S")
    elif "ساعت" in date:
      offset = int(re.sub(r"[^\d]", "", date))
      delta = timedelta(hours=offset)
      return (now - delta).strftime("%Y-%m-%d %H:%M:%S")
    elif "دیروز" in date:
      offset = 1
      return (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    elif "روز پیش" in date:
      offset = int(re.sub(r"[^\d]", "", date))
      return (now - timedelta(days=offset)).strftime("%Y-%m-%d %H:%M:%S")
    return now.strftime("%Y-%m-%d %H:%M:%S")
    
wb = Workbook()
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
  # Sets up the xlsx sheet
  sheet = wb.active
  sheet.title = 'CAR ads Data'
  sheet["A1"] = "Title"
  sheet["B1"] = "Condition"
  sheet["C1"] = "Price"
  sheet["D1"] = "Link"

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
      price = get_digit(price)
      milage = get_digit(milage)

      spans = article.find_elements(By.TAG_NAME, "span")

      date = None

      for span in spans:
          text = span.text.strip()

          if (
              "لحظاتی پیش" in text
              or "دیروز" in text
              or "ساعت پیش" in text
              or "روز پیش" in text
              or re.match(r"^\d{4}/\d{1,2}/\d{1,2}$", fa_to_en(text))
          ):
              date = text
              break

      if date is None:
          date = "لحظاتی پیش"

      date = get_date(date)
      db.sqlite_submit_records(title, link, price, milage, date, "bama")
    except Exception as e:
      print(f"Error in article {i}: {e}")
      continue
    sheet[f"A{i+2}"] = title
    sheet[f"B{i+2}"] = milage
    sheet[f"C{i+2}"] = price
    sheet[f"D{i+2}"] = link
  
  time.sleep(5)
finally:
  wb.save(r".\\output\\ads.xlsx")
  driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
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

wb = Workbook()
URL = "https://bama.ir/car/all/fars-shiraz?installment=0&price=300000000,1500000000&body=passenger_car"
title_selector = "div.inline-flex.mb-1 span.text-neutral-10"
price_selector = 'p.flex.items-center.justify-end.gap-1'
#condition_selector = '//*[@id="__nuxt"]/main/div[1]/div/section/section/div/article[1]/a/div/div/div[1]/div[1]/div[1]/div[3]/span/span[3]'
try:
  driver = webdriver.Edge()
  driver.get(URL)
  time.sleep(2)
  scroll_to_bottom(driver= driver)

  articles = driver.find_elements(By.TAG_NAME, "article")
  sheet = wb.active
  sheet.title = 'CAR ads Data'

  sheet["A1"] = "Title"
  sheet["B1"] = "Condition"
  sheet["C1"] = "Price"
  sheet["D1"] = "Link"
  for i, article in enumerate(articles):
    title = article.find_element(By.CSS_SELECTOR, title_selector).text
    link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
    price = article.find_element(By.CSS_SELECTOR, price_selector).text
    condition = article.find_element(By.CSS_SELECTOR, "span[dir='ltr']").text

    sheet[f"A{i+2}"] = title
    sheet[f"B{i+2}"] = condition
    sheet[f"C{i+2}"] = price
    sheet[f"D{i+2}"] = link

  time.sleep(10)
finally:
  wb.save(r"output\\ads.xlsx")
  driver.quit()

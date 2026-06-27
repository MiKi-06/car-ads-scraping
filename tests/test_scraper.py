from selenium import webdriver
from selenium.webdriver.common.by import By
from scraper.scraper import Scraper

def test_scroll_to_bottom():
  URL = "https://bama.ir/car/all/fars-shiraz"

  driver = webdriver.Edge()
  driver.get(URL)
  scraper = Scraper(db="")

  scraper.scroll_to_bottom(driver=driver, pause_time=3, max_attempts=10)


if __name__ == "__main__": 
  test_scroll_to_bottom()

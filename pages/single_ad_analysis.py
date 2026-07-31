import streamlit as st
import pandas as pd
import time
from scraper.scraper import Scraper
from scraper.database import Database
from analysis import statistics_utils
st.title("Single Ad Analysis")
url = st.text_input("Enter ad URL:", placeholder="https://bama.ir/car/..")

if st.button("Analyze"):
  with st.spinner("Fetching data.."):
    db = Database()
    scraper = Scraper(db=db)
    ad = db.get_ad_by_url(url)
    if ad is None:
      scraper.single_ad_scrape(url)
      ad = db.get_ad_by_url(url)

    ads = db.fetch_ads(ad["model"])

    if len(ads) < 30:
      scraper.scrape_model(ad)
      ads = db.fetch_ads(ad["model"])
      print(len(ads))
      time.sleep(3)
      ads = statistics_utils.clean_ads(ads) 
      print(len(ads))
    else:
      print("analyze")


  df = pd.DataFrame([ad], columns=["id", "model", "year", "milage", "price",
                                  "link", "date", "source"])
  st.dataframe(df, hide_index=True)

  print(type(ads))
  print(ads)

  df = pd.DataFrame(ads, columns=["id", "model", "year", "milage", "price",
                              "link", "date", "source"])
  st.dataframe(df, hide_index=True)


  db.close()
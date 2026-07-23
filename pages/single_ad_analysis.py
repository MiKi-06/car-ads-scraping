import streamlit as st
import pandas as pd
from scraper.scraper import Scraper
from scraper.database import Database
from selenium.common.exceptions import WebDriverException

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
      scraper.scrape_model(ad["model"])
    else:
      print("analyze")


  df = pd.DataFrame([ad], columns=["id", "model", "year", "milage", "price",
                                  "link", "date", "source"])
  st.dataframe(df, hide_index=True)

  


  db.close()
import streamlit as st
import pandas as pd
from scraper.scraper import Scraper
from scraper.database import Database
from selenium.common.exceptions import WebDriverException

st.title("Single Ad Analysis")
url = st.text_input("Enter ad URL:", placeholder="https://bama.ir/car/..")

if st.button("Analyze"):
  db = Database()
  if (ad := db.get_ad_by_url(url)) is not None:
    df = pd.DataFrame([ad], columns=["id", "model", "year", "milage", "price",
                                  "link", "date", "source"])
    st.dataframe(df, hide_index=True)
import streamlit as st
from scraper.scraper import Scraper
from scraper.database import Database
st.title("Collect ADS")

city = st.selectbox("City: ", options=["fars-shiraz"])
min_price = st.number_input("Min-Price:",
                            max_value=100_000_000_000,
                            step=50_000_000, format="%d")
max_price = st.number_input("Max-Price:",
                            max_value=100_000_000_000,
                            step=50_000_000, format="%d")
source = st.radio("Source(s):", ["bama"],)
if st.button("Start Scraping"):
  db = Database()
  scraper = Scraper(min_price, max_price, db, city)

  progress_bar = st.progress(0,"Progress:")
  with st.spinner("Scraping...") as spinner:
    for current, total in scraper.scrape():
      progress_bar.progress(current / total)
  
  st.success("Scraping completed successfully.")
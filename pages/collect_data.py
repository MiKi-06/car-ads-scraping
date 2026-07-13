import streamlit as st
from scraper.scraper import Scraper
from scraper.database import Database

LOCATIONS = ["isfahan-isfahan", "tehran-tehran", "alborz-karaj",
            "azarbaijan_sharghi-tabriz", "razavi_khorasan-mashhad",
            "fars-shiraz"]

st.title("Collect ADS")

city = st.selectbox("City: ", options=LOCATIONS)
min_price = st.number_input("Min-Price:",
                            max_value=100_000_000_000,
                            step=50_000_000, format="%d")
max_price = st.number_input("Max-Price:",
                            max_value=100_000_000_000,
                            step=50_000_000, format="%d")
source = st.radio("Source(s):", ["bama"],)
if st.button("Start Scraping"):
  try:
    db = Database()
    scraper = Scraper(min_price=min_price,max_price=max_price,
                      db=db, city=city)
    progress_bar = st.progress(0,"Progress:")
    with st.spinner("Scraping...") as spinner:
      for current, total in scraper.scrape():
        progress_bar.progress(current / total)
  finally:
    db.close()
    st.success("Scraping completed successfully.")
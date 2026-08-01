import streamlit as st
import pandas as pd
import time
from scraper.scraper import Scraper
from analysis.analysis import Analyzer
from scraper.database import Database
from analysis import statistics_utils
st.title("Single Ad Analysis")
url = st.text_input("Enter ad URL:", placeholder="https://bama.ir/car/..")

if st.button("Analyze"):
  with st.spinner("Fetching data.."):
    db = Database()
    scraper = Scraper(db=db)
    analyzer = Analyzer(db)
    ad = db.get_ad_by_url(url)
    if ad is None:
      scraper.single_ad_scrape(url)
      ad = db.get_ad_by_url(url)

    ads = db.fetch_ads(ad["model"])
    print(ads)
    if len(ads) < 3 or ads is None:
      scraper.scrape_model(ad)
      db.conn.commit()
      scraper.scrape_model(ad)

      print("Rows in DB:", len(db.fetch_ads(ad["model"])))

      print("Model:", ad["model"])

      print(db.fetch_ads(ad["model"])[:3])


    ads = db.fetch_ads(ad["model"])
    print(len(ads))

    result = analyzer.analyze_market(ad["model"])
    stats = result["statistics"]
    rated_deals = result["rated_deals"]

    stats_difference = analyzer.stats_diff(ad, ads)
    price_diff = stats_difference["price_diff"]
    milage_diff = stats_difference["milage_diff"]

    
    print(len(ads))
    
  with st.expander("Market Stats"):
    col1, col2, col3 = st.columns(3)
  
    with col1:
      st.metric(label="Model:", value=stats['model'])
      st.metric(label="Count:", value=stats['count'])
    with col2:
      st.metric(label="ℹ️Median:", value=stats['median'], format="%,d")
      st.metric(label="🔼Highest Price:", value=stats['highest'], format="%,d")
    with col3:
      st.metric(label="▶️Average:", value=stats['average'], format="%,d")
      st.metric(label="🔽Lowest Price:", value=stats['lowest'], format="%,d")

  with st.expander("Result", expanded= True):

    if price_diff is None:
      st.badge(f"This Car's price is Negotiable",
              icon=":material/warning:",color="orange")

    elif price_diff > 50:
      st.badge(f"This Car is cheaper than %{price_diff} of the similar ads",
              icon=":material/done_all:",color="green")
    elif 40 < price_diff < 50:
      st.badge(f"This Car is more expensive than %{price_diff} of the similar ads",
                    icon=":material/warning:",color="red")
    else:
      st.badge(f"This Car has an average Price",
                          icon=":material/check:",color="yellow")

    if milage_diff < 50: 
      st.badge(f"This Car's Mileage is lower than %{milage_diff} of the similar ads",
                    icon=":material/done_all:",color="green")
    elif 40 < milage_diff < 50:
      st.badge(f"This Car has an average Mileage",
                          icon=":material/check:",color="yellow")
    else:
      st.badge(f"This Car's Milage is higher than %{milage_diff} of the similar ads",
                    icon=":material/warning:",color="red")
      
  df = pd.DataFrame([ad], columns=["id", "model", "year", "milage", "price",
                                  "link", "date", "source"])
  st.dataframe(df, hide_index=True)

  df = pd.DataFrame(rated_deals, columns=["id", "score", "model", "year", "milage", "price",
                              "link", "date", "source"])
  df = df.sort_values("score")
  st.dataframe(df, hide_index=True)


  db.close()
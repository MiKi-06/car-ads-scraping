import streamlit as st
import pandas as pd
from scraper.database import Database
from analysis.analysis import Analyzer

db = Database()
analyzer = Analyzer(db)
models = db.fetch_models()

st.title("🚗 Car Market Analyzer")
model = st.selectbox(label="Models", options=models)

if st.button("Analyze"):
  result = analyzer.analyze_market(model)
  stats = result['statistics']
  good_deals = result['good_deals']
  
  df = pd.DataFrame(good_deals, columns=["id", "score", "model", "milage", "price", "link", "date", "source"])
  st.metric(label="Model", value=stats['model'])
  st.metric(label="Count", value=stats['count'])
  st.metric(label="ℹ️Median", value=stats['median'], format="%,d")
  st.metric(label="🔼Highest Price", value=stats['highest'], format="%,d")
  st.metric(label="🔽Lowest Price", value=stats['lowest'], format="%,d")
  st.metric(label="▶️Average", value=stats['average'], format="%,d")

  st.dataframe(df, hide_index=True)

  
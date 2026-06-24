import streamlit as st
import pandas as pd
import plotly.express as px
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
  prices = db.get_prices(model)
  median_price = stats["median"]

  st.metric(label="Model", value=stats['model'])
  st.metric(label="Count", value=stats['count'])
  st.metric(label="ℹ️Median", value=stats['median'], format="%,d")
  st.metric(label="🔼Highest Price", value=stats['highest'], format="%,d")
  st.metric(label="🔽Lowest Price", value=stats['lowest'], format="%,d")
  st.metric(label="▶️Average", value=stats['average'], format="%,d")
  
  df = pd.DataFrame({"prices": prices})

  fig = px.histogram(
    df,
    x="prices",
    nbins=30,
    title=f"Price Distribution - {model}",
  )

  fig.add_vline(
    x=stats["median"],
    line_dash="dash",
    annotation_text=f"Median: {stats['median']:,}",
    annotation_position="top right"
  )

  fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Price (Toman)",
    yaxis_title="Number of Ads",
    title_x=0.5
  )

  fig.update_xaxes(tickformat=",")

  fig.update_traces(
    opacity=0.8,
    marker_line_width=1,
  )
  st.plotly_chart(fig, use_container_width=True)

  df = pd.DataFrame(good_deals, columns=["id", "score", "model",
                                        "milage", "price", "link",
                                        "date", "source"])
  st.dataframe(df, hide_index=True)

  
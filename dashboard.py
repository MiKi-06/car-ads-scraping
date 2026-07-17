import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from scraper.database import Database
from analysis.analysis import Analyzer
from analysis.statistics_utils import remove_outliers

class Dashboard:
  def __init__(self):
    self.db = Database()
    self.analyzer = Analyzer(self.db)
    self.models = self.db.fetch_models()
    self.date_diff = self.get_date_diff()
    self.init()

  def init(self):
    st.title("🚗 Car Market Analyzer")

    if self.date_diff is None:
      st.caption(body="Collect ads first.")
    elif self.date_diff <= 6:
      st.badge("Data is fresh!", icon=":material/done_all:",color="green", 
              help="Data refresh is not needed.")
    elif 6 < self.date_diff <= 12:
      st.badge("Data is fine.", icon=":material/check:",color="yellow", 
              help="Data refresh the data.")
    elif 12 < self.date_diff < 24:
      st.badge("Data is outdated.", icon=":material/warning:",color="orange", 
              help="Data refresh is recommended.")
    else:
      st.badge("Data Needs refreshing!", icon=":material/block:",color="red", 
              help="Data refresh is necessary.")
    
    self.model = st.selectbox(label="Models", options=self.models)
    
    if st.button("Analyze"):
      if self.model is not None:
        result = self.analyzer.analyze_market(self.model)
        stats = result['statistics']
        rated_deals = result['rated_deals']
        prices = self.db.get_prices(self.model)
        prices = remove_outliers(prices)

        median_price = stats["median"]

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

        self.rated_deals_table(rated_deals)
        self.plot_dist_chart(prices, stats)
        self.plot_main_chart()

  def get_date_diff(self):
    pass
    if (last_update:=self.db.get_last_update()):
      now = datetime.now()
      last_update = datetime.fromisoformat(last_update)
      diff = now - last_update
      return diff.total_seconds() / 3600
    else:
      return None

      

  def plot_dist_chart(self, prices, stats):
    with st.expander("🚗 Price Distribution"):
      df = pd.DataFrame({"prices": prices})

      fig = px.histogram(
        df,
        x="prices",
        nbins=30,
        title=f"Price Distribution - {self.model}",
      )

      fig.add_vline(
        x= stats["median"],
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
      st.plotly_chart(fig, width="stretch")

  def plot_main_chart(self):
    with st.expander("🚗 Milage vs Price"):
      ads = self.db.fetch_ads(self.model)

      df = pd.DataFrame(ads)

      fig = px.scatter(
          df,
          x="milage",
          y="price",
          color="price",
          hover_data=["model", "price", "milage","link", "date"],
          title=f"{self.model} Market Analysis"
      )

      fig.update_layout(
          template="plotly_white",
          xaxis_title="Mileage (km)",
          yaxis_title="Price (Toman)",
          height=600
      )

      fig.update_xaxes(tickformat=",")
      fig.update_yaxes(tickformat=",")

      st.plotly_chart(fig, width="stretch")

  def rated_deals_table(self, rated_deals):
    if not rated_deals:
      st.info("No good deal to show.")
      return
    df = pd.DataFrame(rated_deals, columns=["score", "diff_percent", "model",
                                          "year", "milage", "price",
                                          "link", "date", "source"])
    st.subheader("🟢 Ads List")
    df = df.sort_values("score")
    st.dataframe(df, hide_index=True)

def main():
  dash = Dashboard()

if __name__ == "__main__":
  main()
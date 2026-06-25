import streamlit as st

st.title("Collect ADS")

st.selectbox("City: ", options=["fars-shiraz"])
min_price = st.text_input("Min-Price:")
max_price = st.text_input("Max-Price:")
source = st.radio("Source(s):", ["bama"])
if st.button("Start Scraping"):
  st.info(min_price)
  st.info(max_price)
  st.info(source)
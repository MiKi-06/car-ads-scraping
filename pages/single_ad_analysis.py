import streamlit as st
from scraper.scraper import Scraper
from scraper.database import Database
from selenium.common.exceptions import WebDriverException

st.title("Single Ad Analysis")
st.text_input("Enter ad URL:", placeholder="https://bama.ir/car/..")

st.button("Analyze")
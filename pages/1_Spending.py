import streamlit as st
from src.page_builder import render_dataset_page

st.set_page_config(page_title="Spending", layout="wide", page_icon="\U0001f4b3")
render_dataset_page("spending")

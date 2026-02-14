import streamlit as st
from src.page_builder import render_dataset_page

st.set_page_config(page_title="Unemployment Claims", layout="wide", page_icon="\U0001f4ca")
render_dataset_page("unemployment")

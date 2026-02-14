import streamlit as st
from src.page_builder import render_dataset_page

st.set_page_config(page_title="Employment", layout="wide", page_icon="\U0001f454")
render_dataset_page("employment")

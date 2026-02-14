import streamlit as st
from src.page_builder import render_dataset_page

st.set_page_config(page_title="Job Postings", layout="wide", page_icon="\U0001f4cb")
render_dataset_page("job_postings")

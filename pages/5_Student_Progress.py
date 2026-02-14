import streamlit as st
from src.page_builder import render_dataset_page

st.set_page_config(page_title="Student Progress", layout="wide", page_icon="\U0001f4da")
render_dataset_page("student_progress")

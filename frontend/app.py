import streamlit as st
from auth import login
from  layout import layout

st.set_page_config(page_title="Sistema RH", layout="wide", initial_sidebar_state="collapsed")

if "token" not in st.session_state:
    login()
else:
    layout()

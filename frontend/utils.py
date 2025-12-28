import streamlit as st

def handle_auth_error(response):
    if response.status_code in [401, 403]:
        st.error("Acesso negado")
        del st.session_state["token"]
        st.rerun()

import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8086"

def logs_acesso():
    st.title("Logs de Acesso")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4 = st.tabs(["Listar Todos", "Buscar por ID", "Buscar por Usuário", "Buscar por Tempo"])

    with tab1:
        if st.button("Listar Logs"):
            response = requests.get(f"{API_URL}/logs_acesso", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    with tab2:
        log_id = st.number_input("ID Log", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/logs_acesso/{log_id}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.json(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    with tab3:
        id_usuario = st.number_input("ID Usuário", min_value=1, step=1)
        if st.button("Buscar Logs do Usuário"):
            response = requests.get(f"{API_URL}/logs_acesso/usuario/{id_usuario}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    with tab4:
        start_time = st.text_input("Tempo Início (YYYY-MM-DD HH:MM:SS)")
        end_time = st.text_input("Tempo Fim (YYYY-MM-DD HH:MM:SS)")
        if st.button("Buscar por Tempo"):
            response = requests.get(f"{API_URL}/logs_acesso/time_range/?start_time={start_time}&end_time={end_time}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

import streamlit as st
import requests
from utils import handle_auth_error

API_URL = "http://localhost:8086"

def beneficios():
    st.title("Benefícios")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar", "Deletar"])

    with tab1:
        if st.button("Listar Benefícios"):
            response = requests.get(f"{API_URL}/beneficios", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab2:
        with st.form("criar_beneficio"):
            nome = st.text_input("Nome do Benefício")
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {"nome": nome}
                response = requests.post(f"{API_URL}/beneficios", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Benefício criado")
                else:
                    handle_auth_error(response)
                    if response.status_code not in [401, 403]:
                        st.error(f"Erro: {response.text}")

    with tab3:
        beneficio_id = st.number_input("ID Benefício", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/beneficios/{beneficio_id}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.json(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab4:
        with st.form("atualizar_beneficio"):
            beneficio_id = st.number_input("ID Benefício", min_value=1, step=1)
            nome = st.text_input("Novo Nome")
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {"nome": nome}
                response = requests.put(f"{API_URL}/beneficios/{beneficio_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Benefício atualizado")
                else:
                    handle_auth_error(response)
                    if response.status_code not in [401, 403]:
                        st.error(f"Erro: {response.text}")

    # Delete
    with tab5:
        delete_id = st.number_input("ID para Deletar", min_value=1, step=1, key="delete_beneficio")
        if st.button("Deletar"):
            response = requests.delete(f"{API_URL}/beneficios/{delete_id}", headers=headers)
            if response.status_code == 200:
                st.success("Benefício deletado")
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

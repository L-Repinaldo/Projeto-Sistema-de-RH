import streamlit as st
import requests
from utils import handle_auth_error

API_URL = "http://localhost:8086"

def beneficios_funcionarios():
    st.title("Benefícios Funcionários")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar", "Deletar"])

    with tab1:
        if st.button("Listar Benefícios Funcionários"):
            response = requests.get(f"{API_URL}/beneficios-funcionarios", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab2:
        with st.form("criar_beneficio_funcionario"):
            id_funcionario = st.number_input("ID Funcionário", min_value=1, step=1)
            id_beneficio = st.number_input("ID Benefício", min_value=1, step=1)
            ativo = st.checkbox("Ativo", value=True)
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {"id_funcionario": id_funcionario, "id_beneficio": id_beneficio, "ativo": ativo}
                response = requests.post(f"{API_URL}/beneficios-funcionarios", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Benefício Funcionário criado")
                else:
                    handle_auth_error(response)
                    if response.status_code not in [401, 403]:
                        st.error(f"Erro: {response.text}")

    with tab3:
        beneficio_funcionario_id = st.number_input("ID Benefício Funcionário", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/beneficios-funcionarios/{beneficio_funcionario_id}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.json(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab4:
        with st.form("atualizar_beneficio_funcionario"):
            beneficio_funcionario_id = st.number_input("ID Benefício Funcionário", min_value=1, step=1)
            ativo = st.checkbox("Ativo")
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {"ativo": ativo}
                response = requests.put(f"{API_URL}/beneficios-funcionarios/{beneficio_funcionario_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Benefício Funcionário atualizado")
                else:
                    handle_auth_error(response)
                    if response.status_code not in [401, 403]:
                        st.error(f"Erro: {response.text}")

    with tab5:
        beneficio_funcionario_id = st.number_input("ID Benefício Funcionário para Deletar", min_value=1, step=1)
        if st.button("Deletar"):
            response = requests.delete(f"{API_URL}/beneficios-funcionarios/{beneficio_funcionario_id}", headers=headers)
            if response.status_code == 200:
                st.success("Benefício Funcionário deletado")
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

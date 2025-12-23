import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8086"

def funcionarios():
    st.title("Funcionários")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar", "Buscar por Nome", "Buscar por Sobrenome", "Buscar por Setor", "Buscar por Cargo"])

    with tab1:
        if st.button("Listar Funcionários"):
            response = requests.get(f"{API_URL}/funcionarios", headers=headers)
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
        with st.form("criar_funcionario"):
            nome = st.text_input("Nome")
            sobrenome = st.text_input("Sobrenome")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
            data_nascimento = st.date_input("Data Nascimento")
            id_setor = st.number_input("ID Setor", min_value=1, step=1)
            id_cargo = st.number_input("ID Cargo", min_value=1, step=1)
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "telefone": telefone,
                    "data_nascimento": str(data_nascimento),
                    "id_setor": id_setor,
                    "id_cargo": id_cargo
                }
                response = requests.post(f"{API_URL}/funcionarios", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Funcionário criado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab3:
        funcionario_id = st.number_input("ID Funcionário", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/funcionarios/{funcionario_id}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.json(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    with tab4:
        with st.form("atualizar_funcionario"):
            funcionario_id = st.number_input("ID Funcionário", min_value=1, step=1)
            nome = st.text_input("Nome")
            sobrenome = st.text_input("Sobrenome")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
            data_nascimento = st.date_input("Data Nascimento")
            id_setor = st.number_input("ID Setor", min_value=1, step=1)
            id_cargo = st.number_input("ID Cargo", min_value=1, step=1)
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "telefone": telefone,
                    "data_nascimento": str(data_nascimento),
                    "id_setor": id_setor,
                    "id_cargo": id_cargo
                }
                response = requests.put(f"{API_URL}/funcionarios/{funcionario_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Funcionário atualizado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab5:
        nome = st.text_input("Nome")
        if st.button("Buscar por Nome"):
            response = requests.get(f"{API_URL}/funcionarios/nome/{nome}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    with tab6:
        sobrenome = st.text_input("Sobrenome")
        if st.button("Buscar por Sobrenome"):
            response = requests.get(f"{API_URL}/funcionarios/sobrenome/{sobrenome}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    with tab7:
        id_setor = st.number_input("ID Setor", min_value=1, step=1, key="buscar_setor")
        if st.button("Buscar por Setor"):
            response = requests.get(f"{API_URL}/funcionarios/setor/{id_setor}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    with tab8:
        id_cargo = st.number_input("ID Cargo", min_value=1, step=1, key="buscar_cargo")
        if st.button("Buscar por Cargo"):
            response = requests.get(f"{API_URL}/funcionarios/cargo/{id_cargo}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    # Delete
    st.subheader("Deletar Funcionário")
    delete_id = st.number_input("ID para Deletar", min_value=1, step=1, key="delete_funcionario")
    if st.button("Deletar"):
        response = requests.delete(f"{API_URL}/funcionarios/{delete_id}", headers=headers)
        if response.status_code == 200:
            st.success("Funcionário deletado")
        elif response.status_code in [401, 403]:
            st.error("Acesso negado")
            del st.session_state["token"]
            st.rerun()
        else:
            st.error(f"Erro: {response.text}")

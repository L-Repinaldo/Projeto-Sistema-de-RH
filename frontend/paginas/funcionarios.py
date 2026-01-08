import datetime
import streamlit as st
import requests
from datetime import date
from utils import handle_auth_error

API_URL = "http://localhost:8086"

def funcionarios():
    st.title("Funcionários")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    # Fetch options for selectboxes
    try:
        setores_response = requests.get(f"{API_URL}/setores", headers=headers)
        if setores_response.status_code == 200:
            setores = setores_response.json()
            setores_map = {s["nome"]: s["id"] for s in setores}
            setores_names = list(setores_map.keys())
        else:
            setores_names = []
            handle_auth_error(setores_response)

        cargos_response = requests.get(f"{API_URL}/cargos", headers=headers)
        if cargos_response.status_code == 200:
            cargos = cargos_response.json()
            cargos_map = {c["nome"] : c["id"] for c in cargos}
            cargos_names = list(cargos_map.keys())
        else:
            cargos_names = []
            handle_auth_error(cargos_response)

        beneficios_response = requests.get(f"{API_URL}/beneficios", headers=headers)
        if beneficios_response.status_code == 200:
            beneficios = beneficios_response.json()
            beneficios_map = {b["nome"] : b["id"] for b in beneficios}
            beneficios_names = list(beneficios_map.keys())
        else:
            beneficios_names = []
            handle_auth_error(beneficios_response)
    except Exception as e:
        st.error(f"Erro ao carregar opções: {e}")
        setores_names = []
        cargos_names = []
        beneficios_names = []

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar", "Buscar por Nome", "Buscar por Sobrenome", "Buscar por Setor", "Buscar por Cargo", "Deletar"])

    with tab1:
        if st.button("Listar Funcionários"):
            response = requests.get(f"{API_URL}/funcionarios", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab2:
        with st.form("criar_funcionario"):
            nome = st.text_input("Nome")
            sobrenome = st.text_input("Sobrenome")
            email = st.text_input("Email")
            cpf = st.text_input("CPF")
            min_date_birth = datetime.date(1950, 1, 1)
            data_nascimento = st.date_input("Data Nascimento", min_value= min_date_birth)
            min_date_admi = datetime.date(2010, 1, 1)
            data_admissao = st.date_input("Data admissão", min_value = min_date_admi)
            salario = st.number_input("Salário")
            setor = st.selectbox("Setor", options=setores_names, key="criar_setor")
            cargo = st.selectbox("Cargo", options=cargos_names, key="criar_cargo")
            beneficios = st.multiselect("Benefícios", options=beneficios_names, key="criar_beneficios")

            id_setor = setores_map[setor]
            id_cargo = cargos_map[cargo]
            ids_beneficios = [beneficios_map[b] for b in beneficios]


            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "cpf": cpf,
                    "salario" : salario,
                    "data_nascimento": str(data_nascimento),
                    "data_admissao": str(data_admissao),
                    "id_setor": id_setor,
                    "id_cargo": id_cargo,
                    "beneficios": ids_beneficios
                }
                response = requests.post(f"{API_URL}/funcionarios", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Funcionário criado")
                else:
                    handle_auth_error(response)
                    if response.status_code not in [401, 403]:
                        st.error(f"Erro: {response.text}")

    with tab3:
        funcionario_id = st.number_input("ID Funcionário", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/funcionarios/{funcionario_id}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.json(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab4:
        with st.form("atualizar_funcionario"):
            funcionario_id = st.number_input("ID Funcionário", min_value=1, step=1)
            nome = st.text_input("Nome")
            sobrenome = st.text_input("Sobrenome")
            email = st.text_input("Email")
            cpf = st.text_input("CPF")
            data_nascimento = st.date_input("Data Nascimento")
            setor = st.selectbox("Setor", options=setores_names, key="atualizar_setor")
            cargo = st.selectbox("Cargo", options=cargos_names, key="atualizar_cargo")
            salario = st.number_input("Salario")
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {
                    "nome": nome,
                    "sobrenome": sobrenome,
                    "email": email,
                    "cpf": cpf,
                    "data_nascimento": str(data_nascimento),
                    "setor": setor,
                    "cargo": cargo,
                    "salario" : salario
                }
                response = requests.put(f"{API_URL}/funcionarios/{funcionario_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Funcionário atualizado")
                else:
                    handle_auth_error(response)
                    if response.status_code not in [401, 403]:
                        st.error(f"Erro: {response.text}")

    with tab5:
        nome = st.text_input("Nome")
        if st.button("Buscar por Nome"):
            response = requests.get(f"{API_URL}/funcionarios/nome/{nome}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab6:
        sobrenome = st.text_input("Sobrenome")
        if st.button("Buscar por Sobrenome"):
            response = requests.get(f"{API_URL}/funcionarios/sobrenome/{sobrenome}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab7:
        id_setor = st.number_input("ID Setor", min_value=1, step=1, key="buscar_setor")
        if st.button("Buscar por Setor"):
            response = requests.get(f"{API_URL}/funcionarios/setor/{id_setor}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    with tab8:
        id_cargo = st.number_input("ID Cargo", min_value=1, step=1, key="buscar_cargo")
        if st.button("Buscar por Cargo"):
            response = requests.get(f"{API_URL}/funcionarios/cargo/{id_cargo}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

    # Delete
    with tab9:
        delete_id = st.number_input("ID para Deletar", min_value=1, step=1, key="delete_funcionario")
        if st.button("Deletar"):
            response = requests.delete(f"{API_URL}/funcionarios/{delete_id}", headers=headers)
            if response.status_code == 200:
                st.success("Funcionário deletado")
            else:
                handle_auth_error(response)
                if response.status_code not in [401, 403]:
                    st.error(f"Erro: {response.text}")

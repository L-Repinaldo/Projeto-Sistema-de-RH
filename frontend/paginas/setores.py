import streamlit as st
import requests

API_URL = "http://localhost:8086"

def setores():
    st.title("Setores")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar", "Deletar"])

    with tab1:
        if st.button("Listar Setores"):
            response = requests.get(f"{API_URL}/setores", headers=headers)
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
        with st.form("criar_setor"):
            nome = st.text_input("Nome do Setor")
            id_gerente = st.number_input("ID Gerente", min_value=1, step=1)
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {"nome": nome, "id_gerente": id_gerente}
                response = requests.post(f"{API_URL}/setores", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Setor criado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab3:
        setor_id = st.number_input("ID Setor", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/setores/{setor_id}", headers=headers)
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
        with st.form("atualizar_setor"):
            setor_id = st.number_input("ID Setor", min_value=1, step=1)
            nome = st.text_input("Novo Nome")
            id_gerente = st.number_input("Novo ID Gerente", min_value=1, step=1)
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {"nome": nome, "id_gerente": id_gerente}
                response = requests.put(f"{API_URL}/setores/{setor_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Setor atualizado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab5:
        setor_id = st.number_input("ID Setor para Deletar", min_value=1, step=1)
        if st.button("Deletar"):
            response = requests.delete(f"{API_URL}/setores/{setor_id}", headers=headers)
            if response.status_code == 200:
                st.success("Setor deletado")
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

import streamlit as st
import requests

API_URL = "http://localhost:8086"

def permissoes():
    st.title("Permissões")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar", "Ativar/Desativar"])

    with tab1:
        if st.button("Listar Permissões"):
            response = requests.get(f"{API_URL}/permissoes", headers=headers)
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
        with st.form("criar_permissao"):
            nome = st.text_input("Nome da Permissão")
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {"nome": nome}
                response = requests.post(f"{API_URL}/permissoes", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Permissão criada")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab3:
        permissao_id = st.number_input("ID Permissão", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/permissoes/{permissao_id}", headers=headers)
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
        with st.form("atualizar_permissao"):
            permissao_id = st.number_input("ID Permissão", min_value=1, step=1)
            nome = st.text_input("Novo Nome")
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {"nome": nome}
                response = requests.put(f"{API_URL}/permissoes/{permissao_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Permissão atualizada")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab5:
        permissao_id = st.number_input("ID Permissão para Ativar/Desativar", min_value=1, step=1, key="activate_permissao")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Desativar"):
                response = requests.put(f"{API_URL}/permissoes/{permissao_id}/desactivate", headers=headers)
                if response.status_code == 200:
                    st.success("Permissão desativada")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")
        with col2:
            if st.button("Ativar"):
                response = requests.put(f"{API_URL}/permissoes/{permissao_id}/activate", headers=headers)
                if response.status_code == 200:
                    st.success("Permissão ativada")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

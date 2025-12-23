import streamlit as st
import requests

API_URL = "http://localhost:8086"

def cargos():
    st.title("Cargos")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar", "Ativar/Desativar"])

    with tab1:
        if st.button("Listar Cargos"):
            response = requests.get(f"{API_URL}/cargos", headers=headers)
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
        with st.form("criar_cargo"):
            nome = st.text_input("Nome do Cargo")
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {"nome": nome}
                response = requests.post(f"{API_URL}/cargos", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Cargo criado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab3:
        cargo_id = st.number_input("ID Cargo", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/cargos/{cargo_id}", headers=headers)
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
        with st.form("atualizar_cargo"):
            cargo_id = st.number_input("ID Cargo", min_value=1, step=1)
            nome = st.text_input("Novo Nome")
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {"nome": nome}
                response = requests.put(f"{API_URL}/cargos/{cargo_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Cargo atualizado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab5:
        cargo_id = st.number_input("ID Cargo para Ativar/Desativar", min_value=1, step=1, key="activate_cargo")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Desativar"):
                response = requests.put(f"{API_URL}/cargos/{cargo_id}/desactivate", headers=headers)
                if response.status_code == 200:
                    st.success("Cargo desativado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")
        with col2:
            if st.button("Ativar"):
                response = requests.put(f"{API_URL}/cargos/{cargo_id}/activate", headers=headers)
                if response.status_code == 200:
                    st.success("Cargo ativado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

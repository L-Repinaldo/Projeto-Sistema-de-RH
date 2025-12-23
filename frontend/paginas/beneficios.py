import streamlit as st
import requests

API_URL = "http://localhost:8086"

def beneficios():
    st.title("Benefícios")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar"])

    with tab1:
        if st.button("Listar Benefícios"):
            response = requests.get(f"{API_URL}/beneficios", headers=headers)
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
        with st.form("criar_beneficio"):
            nome = st.text_input("Nome do Benefício")
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {"nome": nome}
                response = requests.post(f"{API_URL}/beneficios", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Benefício criado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab3:
        beneficio_id = st.number_input("ID Benefício", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/beneficios/{beneficio_id}", headers=headers)
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
        with st.form("atualizar_beneficio"):
            beneficio_id = st.number_input("ID Benefício", min_value=1, step=1)
            nome = st.text_input("Novo Nome")
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {"nome": nome}
                response = requests.put(f"{API_URL}/beneficios/{beneficio_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Benefício atualizado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    # Delete
    st.subheader("Deletar Benefício")
    delete_id = st.number_input("ID para Deletar", min_value=1, step=1, key="delete_beneficio")
    if st.button("Deletar"):
        response = requests.delete(f"{API_URL}/beneficios/{delete_id}", headers=headers)
        if response.status_code == 200:
            st.success("Benefício deletado")
        elif response.status_code in [401, 403]:
            st.error("Acesso negado")
            del st.session_state["token"]
            st.rerun()
        else:
            st.error(f"Erro: {response.text}")

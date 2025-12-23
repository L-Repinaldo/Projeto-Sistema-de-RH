import streamlit as st
import requests

API_URL = "http://localhost:8086"

def usuarios():
    st.title("Usuários")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4 = st.tabs(["Listar Todos", "Criar", "Buscar por ID", "Atualizar"])

    with tab1:
        if st.button("Listar Usuários"):
            response = requests.get(f"{API_URL}/usuarios", headers=headers)
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
        with st.form("criar_usuario"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            id_permissao = st.number_input("ID Permissão", min_value=1, step=1)
            id_funcionario = st.number_input("ID Funcionário", min_value=1, step=1)
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {
                    "username": username,
                    "password": password,
                    "id_permissao": id_permissao,
                    "id_funcionario": id_funcionario
                }
                response = requests.post(f"{API_URL}/usuarios", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Usuário criado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab3:
        usuario_id = st.number_input("ID Usuário", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/usuarios/{usuario_id}", headers=headers)
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
        with st.form("atualizar_usuario"):
            usuario_id = st.number_input("ID Usuário", min_value=1, step=1)
            username = st.text_input("Novo Username")
            password = st.text_input("Nova Password", type="password")
            id_permissao = st.number_input("Novo ID Permissão", min_value=1, step=1)
            id_funcionario = st.number_input("Novo ID Funcionário", min_value=1, step=1)
            submitted = st.form_submit_button("Atualizar")
            if submitted:
                payload = {
                    "username": username,
                    "password": password,
                    "id_permissao": id_permissao,
                    "id_funcionario": id_funcionario
                }
                response = requests.put(f"{API_URL}/usuarios/{usuario_id}", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Usuário atualizado")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    # Delete
    st.subheader("Deletar Usuário")
    delete_id = st.number_input("ID para Deletar", min_value=1, step=1, key="delete_usuario")
    if st.button("Deletar"):
        response = requests.delete(f"{API_URL}/usuarios/{delete_id}", headers=headers)
        if response.status_code == 200:
            st.success("Usuário deletado")
        elif response.status_code in [401, 403]:
            st.error("Acesso negado")
            del st.session_state["token"]
            st.rerun()
        else:
            st.error(f"Erro: {response.text}")

import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8086"

def avaliacoes():
    st.title("Avaliações")

    headers = {"Authorization": f"Bearer {st.session_state['token']}"}

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Listar Todas", "Criar", "Buscar por ID", "Buscar por Funcionário", "Buscar por Data", "Buscar por Nota"])

    with tab1:
        if st.button("Listar Avaliações"):
            response = requests.get(f"{API_URL}/avaliacoes", headers=headers)
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
        with st.form("criar_avaliacao"):
            id_funcionario = st.number_input("ID Funcionário", min_value=1, step=1)
            nota = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1)
            comentario = st.text_area("Comentário")
            data_avaliacao = st.date_input("Data Avaliação", value=date.today())
            submitted = st.form_submit_button("Criar")
            if submitted:
                payload = {
                    "id_funcionario": id_funcionario,
                    "nota": nota,
                    "comentario": comentario,
                    "data_avaliacao": str(data_avaliacao)
                }
                response = requests.post(f"{API_URL}/avaliacoes", json=payload, headers=headers)
                if response.status_code == 200:
                    st.success("Avaliação criada")
                elif response.status_code in [401, 403]:
                    st.error("Acesso negado")
                    del st.session_state["token"]
                    st.rerun()
                else:
                    st.error(f"Erro: {response.text}")

    with tab3:
        avaliacao_id = st.number_input("ID Avaliação", min_value=1, step=1)
        if st.button("Buscar"):
            response = requests.get(f"{API_URL}/avaliacoes/{avaliacao_id}", headers=headers)
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
        id_funcionario = st.number_input("ID Funcionário", min_value=1, step=1)
        if st.button("Buscar Avaliações do Funcionário"):
            response = requests.get(f"{API_URL}/avaliacoes/funcionario/{id_funcionario}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                st.dataframe(data)
            elif response.status_code in [401, 403]:
                st.error("Acesso negado")
                del st.session_state["token"]
                st.rerun()
            else:
                st.error(f"Erro: {response.text}")

    with tab5:
        start_date = st.date_input("Data Início")
        end_date = st.date_input("Data Fim")
        if st.button("Buscar por Data"):
            response = requests.get(f"{API_URL}/avaliacoes/date_range/?start_date={start_date}&end_date={end_date}", headers=headers)
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
        min_nota = st.number_input("Nota Mínima", min_value=0.0, max_value=10.0, step=0.1)
        max_nota = st.number_input("Nota Máxima", min_value=0.0, max_value=10.0, step=0.1)
        if st.button("Buscar por Nota"):
            response = requests.get(f"{API_URL}/avaliacoes/nota_range/?min_nota={min_nota}&max_nota={max_nota}", headers=headers)
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
    st.subheader("Deletar Avaliação")
    delete_id = st.number_input("ID para Deletar", min_value=1, step=1, key="delete_avaliacao")
    if st.button("Deletar"):
        response = requests.delete(f"{API_URL}/avaliacoes/{delete_id}", headers=headers)
        if response.status_code == 200:
            st.success("Avaliação deletada")
        elif response.status_code in [401, 403]:
            st.error("Acesso negado")
            del st.session_state["token"]
            st.rerun()
        else:
            st.error(f"Erro: {response.text}")

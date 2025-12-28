import streamlit as st, requests

API_URL = "http://localhost:8086"

def login():

    st.title("Login")

    username = st.text_input("Username: ")
    password = st.text_input("Senha: ") 

    if st.button("Entrar"):

        response = requests.post(
            f"{API_URL}/usuarios/login",
            json ={
                "username" : username,
                "password" : password
                }
        )

        if response.status_code == 200:

            data = response.json()

            st.session_state["token"] = data["access_token"]
            st.session_state["user"] = data["usuario"]
            st.session_state["permissao"] = data["permissao"]

            st.success("Login realizado")
            st.rerun()
            
        else:
            st.error("Credenciais inválidas")


import streamlit as st
import requests

API_URL = "http://localhost:8086"


def administracao():
    st.title("⚠️ Administração do Sistema")

    # Segurança básica no front
    if "token" not in st.session_state:
        st.error("Acesso não autorizado.")
        return

    headers = {
        "Authorization": f"Bearer {st.session_state['token']}"
    }

    st.warning(
        "Esta ação irá popular o sistema com dados fictícios.\n\n"
        "Use apenas para testes e desenvolvimento."
    )

    qtd_funcionarios = st.number_input(
        "Quantidade de funcionários",
        min_value=1,
        max_value=5000,
        step=10,
        value=100
    )

    confirmar = st.checkbox("Confirmo que desejo popular o sistema")

    if st.button("🚀 Popular Sistema"):
        if not confirmar:
            st.error("Confirme a ação antes de continuar.")
            return

        with st.spinner("Populando o sistema... Isso pode levar alguns segundos."):
            response = requests.post(
                f"{API_URL}/admin/populacao/sistema",
                params={"qtd_funcionarios": int(qtd_funcionarios)},
                headers=headers
            )

        if response.status_code == 200:
            data = response.json()
            st.success(
                f"Sistema populado com sucesso!\n\n"
                f"Funcionários criados: {data['funcionarios_criados']}"
            )
        elif response.status_code in [401, 403]:
            st.error("Acesso negado.")
            del st.session_state["token"]
            st.rerun()
        else:
            st.error(f"Erro: {response.text}")

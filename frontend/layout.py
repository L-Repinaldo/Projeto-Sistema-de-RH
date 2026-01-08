import streamlit as st

def layout():
    st.sidebar.title("Navegação")

    pages = [
        "Funcionários",
        "Avaliações",
        "Benefícios",
        "Cargos",
        "Setores",
        "Usuários",
        "Permissões",
        "Logs Acesso",
        "Benefícios Funcionários"
    ]

    if st.session_state.get("permissao") == "ADMIN":
        pages.append("Administração")

    page = st.sidebar.selectbox(
        "Selecione uma página",
        pages
    )

    match page:
        case "Funcionários":
            from paginas import funcionarios
            funcionarios.funcionarios()

        case "Avaliações":
            from paginas import avaliacoes
            avaliacoes.avaliacoes()

        case "Benefícios":
            from paginas import beneficios
            beneficios.beneficios()

        case "Cargos":
            from paginas import cargos
            cargos.cargos()

        case "Setores":
            from paginas import setores
            setores.setores()

        case "Usuários":
            from paginas import usuarios
            usuarios.usuarios()

        case "Permissões":
            from paginas import permissoes
            permissoes.permissoes()

        case "Logs Acesso":
            from paginas import logs_acesso
            logs_acesso.logs_acesso()

        case "Benefícios Funcionários":
            from paginas import beneficios_funcionarios
            beneficios_funcionarios.beneficios_funcionarios()

        case "Administração":
            from paginas import administracao
            administracao.administracao()

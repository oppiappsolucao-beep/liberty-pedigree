import streamlit as st

st.set_page_config(
    page_title="Liberty Pedigree",
    page_icon="🐶",
    layout="wide"
)

USUARIOS = {
    "liberty": {
        "senha": "123456",
        "nome": "Liberty Pedigree",
        "tipo": "admin"
    }
}


def aplicar_css():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                linear-gradient(
                    135deg,
                    rgba(245, 247, 245, 0.75) 0%,
                    rgba(232, 241, 234, 0.75) 42%,
                    rgba(213, 232, 219, 0.75) 100%
                );
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(
                    180deg,
                    rgba(10, 77, 44, 0.75) 0%,
                    rgba(15, 107, 62, 0.75) 48%,
                    rgba(6, 54, 31, 0.75) 100%
                ) !important;
            border-right: 1px solid rgba(255,255,255,0.15);
        }

        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }

        .block-container {
            padding-top: 2rem !important;
        }

        .login-card {
            max-width: 430px;
            margin: 80px auto 0 auto;
            padding: 36px;
            border-radius: 24px;
            background: rgba(255, 255, 255, 0.92);
            box-shadow: 0 20px 50px rgba(10, 77, 44, 0.18);
            border: 1px solid rgba(15, 107, 62, 0.18);
            text-align: center;
            backdrop-filter: blur(8px);
        }

        .login-badge {
            display: inline-block;
            padding: 8px 14px;
            border-radius: 999px;
            background: rgba(212, 160, 23, 0.14);
            color: #0A4D2C;
            font-weight: 800;
            font-size: 13px;
            margin-bottom: 14px;
        }

        .login-title {
            font-size: 36px;
            font-weight: 900;
            color: #0A4D2C;
            margin-bottom: 6px;
        }

        .login-subtitle {
            font-size: 15px;
            color: #64748B;
            margin-bottom: 0;
        }

        label, .stTextInput label {
            color: #0A4D2C !important;
            font-weight: 700 !important;
        }

        div.stButton > button {
            width: 100%;
            height: 46px;
            border-radius: 12px;
            border: none;
            background: #D4A017;
            color: #FFFFFF;
            font-weight: 800;
            font-size: 16px;
        }

        div.stButton > button:hover {
            background: #B88912;
            color: #FFFFFF;
            border: none;
        }

        .top-card {
            padding: 28px;
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(15, 107, 62, 0.15);
            box-shadow: 0 12px 35px rgba(10, 77, 44, 0.08);
            backdrop-filter: blur(8px);
        }

        .top-title {
            font-size: 34px;
            font-weight: 900;
            color: #0A4D2C;
            margin-bottom: 4px;
        }

        .top-subtitle {
            color: #64748B;
            font-size: 16px;
        }

        .page-box {
            padding: 24px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(15, 107, 62, 0.12);
            box-shadow: 0 8px 25px rgba(10, 77, 44, 0.06);
            backdrop-filter: blur(8px);
        }

        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.92);
            padding: 18px;
            border-radius: 18px;
            border: 1px solid rgba(15, 107, 62, 0.14);
            box-shadow: 0 8px 20px rgba(10, 77, 44, 0.05);
            backdrop-filter: blur(8px);
        }

        [data-testid="stMetric"] label {
            color: #0A4D2C !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricValue"] {
            color: #0A4D2C !important;
            font-weight: 900 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def iniciar_sessao():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if "usuario" not in st.session_state:
        st.session_state.usuario = None

    if "nome_usuario" not in st.session_state:
        st.session_state.nome_usuario = None

    if "tipo_usuario" not in st.session_state:
        st.session_state.tipo_usuario = None


def fazer_login(usuario, senha):
    usuario = usuario.strip().lower()

    if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
        st.session_state.logado = True
        st.session_state.usuario = usuario
        st.session_state.nome_usuario = USUARIOS[usuario]["nome"]
        st.session_state.tipo_usuario = USUARIOS[usuario]["tipo"]
        st.rerun()
    else:
        st.error("Usuário ou senha incorretos.")


def fazer_logout():
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.nome_usuario = None
    st.session_state.tipo_usuario = None
    st.rerun()


def tela_login():
    st.markdown(
        """
        <div class="login-card">
            <div class="login-badge">Dashboard Operacional</div>
            <div class="login-title">🐶 Liberty Pedigree</div>
            <div class="login-subtitle">Acesse o painel de controle</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 1.1, 1])

    with col2:
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            fazer_login(usuario, senha)


def tela_visao_geral():
    st.subheader("📊 Visão Geral")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Pedigrees recebidos", "0")
    col2.metric("Em produção", "0")
    col3.metric("Finalizados", "0")
    col4.metric("Pendências", "0")

    st.write("")

    st.markdown(
        """
        <div class="page-box">
            Esta é a página de visão geral. Aqui vamos colocar os indicadores, gráficos e resumo da operação.
        </div>
        """,
        unsafe_allow_html=True
    )


def tela_formulario():
    st.subheader("📝 Formulário")

    st.markdown(
        """
        <div class="page-box">
            Aqui vamos criar o formulário para cadastrar novos pedidos de pedigree.
        </div>
        """,
        unsafe_allow_html=True
    )


def tela_producao():
    st.subheader("⚙️ Produção")

    st.markdown(
        """
        <div class="page-box">
            Aqui vamos acompanhar os pedidos cadastrados e o status da produção.
        </div>
        """,
        unsafe_allow_html=True
    )


def tela_dashboard():
    with st.sidebar:
        st.markdown("## 🐶 Liberty")
        st.markdown("**Pedigree**")
        st.markdown("---")

        pagina = st.radio(
            "Menu",
            [
                "Visão Geral",
                "Formulário",
                "Produção"
            ]
        )

        st.markdown("---")

        if st.button("Sair"):
            fazer_logout()

    st.markdown(
        """
        <div class="top-card">
            <div class="top-title">Liberty Pedigree</div>
            <div class="top-subtitle">Painel operacional de controle e acompanhamento</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if pagina == "Visão Geral":
        tela_visao_geral()

    elif pagina == "Formulário":
        tela_formulario()

    elif pagina == "Produção":
        tela_producao()


def main():
    aplicar_css()
    iniciar_sessao()

    if st.session_state.logado:
        tela_dashboard()
    else:
        tela_login()


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import uuid
import base64
from pathlib import Path

st.set_page_config(
    page_title="Liberty Pedigree",
    page_icon="🐶",
    layout="wide"
)

SHEET_ID = "1qkhbn11yyaaXniRpoZd0CfG0T3LF9hJT1kRTh2foVmM"
ABA_BASE = "Base"

STATUS_OPCOES = [
    "Novo Lead",
    "Conversando",
    "Não Tem Interesse",
    "Não Responde",
    "Alteração"
]

USUARIOS = {
    "liberty": {
        "senha": "123456",
        "nome": "Liberty Pedigree",
        "tipo": "admin"
    }
}

COLUNAS_BASE = [
    "ID",
    "Data Cadastro",
    "Status",
    "Vendedor",
    "Nome Tutor",
    "CPF Tutor",
    "Telefone Tutor",
    "Email Tutor",
    "Rua Avenida",
    "Numero",
    "Complemento",
    "Bairro",
    "Cidade",
    "Estado",
    "CEP",
    "Nome Animal",
    "Data Nascimento Animal",
    "Raca",
    "Sexo",
    "Cor Pelagem",
    "Pelagem",
    "Microchip",
    "Proprietario Contrato",
    "Nome Transferencia",
    "CPF Transferencia",
    "Email Transferencia",
    "Telefone Transferencia",
    "Observacao Transferencia",
    "Observacao Interna",
    "Data Alteracao"
]


def image_to_base64(caminho):
    arquivo = Path(caminho)
    if not arquivo.exists():
        return ""
    return base64.b64encode(arquivo.read_bytes()).decode("utf-8")


def aplicar_css():
    logo_b64 = image_to_base64("assets/logo-liberty.png")
    login_b64 = image_to_base64("assets/login-pet.png")

    st.markdown(
        f"""
        <style>
        :root {{
            --verde: #0A4D2C;
            --verde2: #0F6B3E;
            --dourado: #D4A017;
            --dourado2: #B88912;
            --texto: #1F2937;
            --cinza: #64748B;
        }}

        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(212, 160, 23, 0.32) 0%, transparent 28%),
                radial-gradient(circle at bottom right, rgba(10, 77, 44, 0.45) 0%, transparent 34%),
                linear-gradient(135deg, #F8FAF7 0%, #FFF8E1 52%, #E7F3EA 100%);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(
                    180deg,
                    rgba(10, 77, 44, 0.92) 0%,
                    rgba(15, 107, 62, 0.92) 48%,
                    rgba(6, 54, 31, 0.92) 100%
                ) !important;
            border-right: 1px solid rgba(255,255,255,0.20);
        }}

        [data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}

        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }}

        .login-wrapper {{
            max-width: 1480px;
            min-height: 820px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid rgba(15, 23, 42, 0.10);
            border-radius: 18px;
            box-shadow: 0 26px 70px rgba(15, 23, 42, 0.12);
            overflow: hidden;
            display: grid;
            grid-template-columns: 46% 54%;
        }}

        .login-left {{
            padding: 58px 92px 40px 92px;
            min-height: 820px;
            position: relative;
            background:
                radial-gradient(circle at 18% 10%, rgba(10, 77, 44, 0.05), transparent 18%),
                linear-gradient(180deg, rgba(255,255,255,0.96), rgba(248,250,252,0.92));
        }}

        .login-logo {{
            width: 112px;
            height: 112px;
            object-fit: contain;
            display: block;
            margin: 0 auto 18px auto;
        }}

        .login-brand {{
            text-align: center;
            color: var(--verde);
            font-size: 48px;
            line-height: 1;
            letter-spacing: 12px;
            font-weight: 400;
            margin-bottom: 10px;
        }}

        .login-brand-sub {{
            text-align: center;
            color: var(--verde);
            font-size: 23px;
            font-weight: 400;
            margin-bottom: 22px;
        }}

        .login-line {{
            width: 58px;
            height: 2px;
            background: var(--dourado);
            margin: 0 auto 25px auto;
        }}

        .login-call {{
            text-align: center;
            color: var(--texto);
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 28px;
        }}

        .login-footer {{
            position: absolute;
            bottom: 36px;
            left: 92px;
            right: 92px;
            color: #8A94A6;
            font-size: 12px;
            text-align: center;
        }}

        .login-right {{
            min-height: 820px;
            background-image: url("data:image/png;base64,{login_b64}");
            background-size: cover;
            background-position: center;
        }}

        .login-google-fake {{
            height: 52px;
            border: 1px solid #E5E7EB;
            border-radius: 9px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
            color: #1F2937;
            font-weight: 600;
            background: rgba(255,255,255,0.92);
            margin-top: 18px;
        }}

        .login-ou {{
            display: flex;
            align-items: center;
            gap: 14px;
            color: #6B7280;
            font-size: 13px;
            margin-top: 24px;
        }}

        .login-ou:before,
        .login-ou:after {{
            content: "";
            flex: 1;
            height: 1px;
            background: #E5E7EB;
        }}

        .login-card, .top-card, .page-box {{
            background: rgba(255, 255, 255, 0.93);
            border: 1px solid rgba(255, 255, 255, 0.55);
            box-shadow: 0 12px 35px rgba(10, 77, 44, 0.15);
            backdrop-filter: blur(8px);
        }}

        .top-card {{
            padding: 28px;
            border-radius: 22px;
        }}

        .top-title {{
            font-size: 34px;
            font-weight: 900;
            color: #0A4D2C;
            margin-bottom: 4px;
        }}

        .top-subtitle {{
            color: #64748B;
            font-size: 16px;
        }}

        .page-box {{
            padding: 24px;
            border-radius: 20px;
        }}

        label, .stTextInput label, .stSelectbox label, .stTextArea label, .stDateInput label {{
            color: #0A4D2C !important;
            font-weight: 700 !important;
        }}

        input {{
            border-radius: 9px !important;
            min-height: 46px !important;
        }}

        div.stButton > button {{
            width: 100%;
            height: 54px;
            border-radius: 9px;
            border: none;
            background: linear-gradient(135deg, #06451F 0%, #0A5A2C 100%);
            color: #FFFFFF;
            font-weight: 800;
            font-size: 16px;
            box-shadow: 0 10px 22px rgba(10, 77, 44, 0.20);
        }}

        div.stButton > button:hover {{
            background: linear-gradient(135deg, #083B20 0%, #06451F 100%);
            color: #FFFFFF;
            border: none;
        }}

        [data-testid="stMetric"] {{
            background: rgba(255, 255, 255, 0.93);
            padding: 18px;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.55);
            box-shadow: 0 8px 20px rgba(10, 77, 44, 0.12);
            backdrop-filter: blur(8px);
        }}

        [data-testid="stMetric"] label {{
            color: #0A4D2C !important;
            font-weight: 700 !important;
        }}

        [data-testid="stMetricValue"] {{
            color: #0A4D2C !important;
            font-weight: 900 !important;
        }}

        @media (max-width: 980px) {{
            .login-wrapper {{
                grid-template-columns: 1fr;
                min-height: auto;
            }}
            .login-right {{
                display: none;
            }}
            .login-left {{
                min-height: auto;
                padding: 40px 28px;
            }}
            .login-footer {{
                position: static;
                margin-top: 40px;
            }}
            .login-brand {{
                font-size: 38px;
                letter-spacing: 8px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

@st.cache_resource
def conectar_google():
    credentials = Credentials.from_service_account_info(
        {
            "type": st.secrets["GOOGLE_TYPE"],
            "project_id": st.secrets["GOOGLE_PROJECT_ID"],
            "private_key_id": st.secrets["GOOGLE_PRIVATE_KEY_ID"],
            "private_key": st.secrets["GOOGLE_PRIVATE_KEY"],
            "client_email": st.secrets["GOOGLE_CLIENT_EMAIL"],
            "client_id": st.secrets["GOOGLE_CLIENT_ID"],
            "auth_uri": st.secrets["GOOGLE_AUTH_URI"],
            "token_uri": st.secrets["GOOGLE_TOKEN_URI"],
            "auth_provider_x509_cert_url": st.secrets["GOOGLE_AUTH_PROVIDER_X509_CERT_URL"],
            "client_x509_cert_url": st.secrets["GOOGLE_CLIENT_X509_CERT_URL"],
        },
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )

    return gspread.authorize(credentials)


def abrir_aba():
    gc = conectar_google()
    planilha = gc.open_by_key(SHEET_ID)
    return planilha.worksheet(ABA_BASE)


def carregar_base():
    aba = abrir_aba()
    dados = aba.get_all_records()
    df = pd.DataFrame(dados)

    for coluna in COLUNAS_BASE:
        if coluna not in df.columns:
            df[coluna] = ""

    return df[COLUNAS_BASE]


def salvar_registro(dados):
    aba = abrir_aba()
    linha = [dados.get(coluna, "") for coluna in COLUNAS_BASE]
    aba.append_row(linha, value_input_option="USER_ENTERED")
    st.cache_data.clear()


def atualizar_status(id_registro, novo_status):
    aba = abrir_aba()
    valores = aba.get_all_values()

    if not valores:
        return False

    cabecalho = valores[0]

    if "ID" not in cabecalho or "Status" not in cabecalho or "Data Alteracao" not in cabecalho:
        return False

    coluna_id = cabecalho.index("ID") + 1
    coluna_status = cabecalho.index("Status") + 1
    coluna_data_alteracao = cabecalho.index("Data Alteracao") + 1

    for indice, linha in enumerate(valores[1:], start=2):
        if len(linha) >= coluna_id and linha[coluna_id - 1] == id_registro:
            aba.update_cell(indice, coluna_status, novo_status)
            aba.update_cell(indice, coluna_data_alteracao, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            st.cache_data.clear()
            return True

    return False


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
    logo_b64 = image_to_base64("assets/logo-liberty.png")

    col_esq, col_dir = st.columns([0.46, 0.54], gap="large")

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    with col_esq:
        st.markdown(
            f"""
            <div class="login-left">
                <img src="data:image/png;base64,{logo_b64}" class="login-logo" />
                <div class="login-brand">LIBERTY</div>
                <div class="login-brand-sub">Pedigrees e Canis Certificados</div>
                <div class="login-line"></div>
                <div class="login-call">Acesse sua conta para continuar</div>
            """,
            unsafe_allow_html=True
        )

        usuario = st.text_input("E-mail ou CPF", placeholder="Digite seu e-mail ou CPF")
        senha = st.text_input("Senha", placeholder="Digite sua senha", type="password")

        st.markdown(
            """
            <div style="text-align:right; color:#0A4D2C; font-size:14px; margin-top:-4px; margin-bottom:18px;">
                Esqueceu sua senha?
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Entrar"):
            fazer_login(usuario, senha)

        st.markdown(
            """
                <div class="login-ou">ou</div>
                <div class="login-google-fake">
                    <span style="font-size:22px; font-weight:900; color:#4285F4;">G</span>
                    <span>Entrar com Google</span>
                </div>
                <div class="login-footer">
                    © 2024 Liberty Pedigrees e Canis Certificados. Todos os direitos reservados.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_dir:
        st.markdown('<div class="login-right"></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def tela_visao_geral():
    st.subheader("📊 Visão Geral")

    df = carregar_base()

    total_recebidos = len(df)
    total_producao = len(df[df["Status"].astype(str).str.strip() == "Conversando"])
    total_finalizados = 0
    total_pendencias = len(df[df["Status"].astype(str).str.strip().isin(["Não Responde", "Alteração"])])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pedigrees recebidos", total_recebidos)
    col2.metric("Em produção", total_producao)
    col3.metric("Finalizados", total_finalizados)
    col4.metric("Pendências", total_pendencias)

    st.write("")

    st.markdown('<div class="page-box">', unsafe_allow_html=True)
    st.markdown("### Buscar cliente")

    busca = st.text_input("Buscar por Nome, CPF, Telefone ou Microchip")

    if busca:
        busca_normalizada = busca.lower().strip()

        df_filtrado = df[
            df["Nome Tutor"].astype(str).str.lower().str.contains(busca_normalizada, na=False) |
            df["CPF Tutor"].astype(str).str.lower().str.contains(busca_normalizada, na=False) |
            df["Telefone Tutor"].astype(str).str.lower().str.contains(busca_normalizada, na=False) |
            df["Microchip"].astype(str).str.lower().str.contains(busca_normalizada, na=False)
        ]

        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
    else:
        st.info("Use o campo acima para localizar um cliente.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    st.markdown("### Cards por Status")

    cols = st.columns(len(STATUS_OPCOES))

    for i, status in enumerate(STATUS_OPCOES):
        qtd = len(df[df["Status"].astype(str).str.strip() == status])
        cols[i].metric(status, qtd)


def tela_formulario():
    st.subheader("📝 Formulário")

    with st.form("formulario_pedigree", clear_on_submit=True):
        st.markdown("### Dados do Tutor")

        col1, col2 = st.columns(2)
        nome_tutor = col1.text_input("Nome completo do tutor")
        cpf_tutor = col2.text_input("CPF")

        col3, col4 = st.columns(2)
        telefone_tutor = col3.text_input("Telefone")
        email_tutor = col4.text_input("E-mail")

        st.markdown("---")
        st.markdown("### Endereço de Envio")

        col5, col6 = st.columns([2, 1])
        rua_av = col5.text_input("Rua / Avenida")
        numero = col6.text_input("Número")

        col7, col8 = st.columns(2)
        complemento = col7.text_input("Complemento")
        bairro = col8.text_input("Bairro")

        col9, col10, col11 = st.columns([2, 1, 1])
        cidade = col9.text_input("Cidade")
        estado = col10.text_input("Estado")
        cep = col11.text_input("CEP")

        st.markdown("---")
        st.markdown("### Dados do Animal")

        col12, col13 = st.columns(2)
        nome_animal = col12.text_input("Nome do animal com sobrenome")
        data_nascimento = col13.date_input("Data de nascimento", format="DD/MM/YYYY")

        col14, col15, col16 = st.columns(3)
        raca = col14.text_input("Raça")
        sexo = col15.selectbox("Sexo", ["", "Macho", "Fêmea"])
        cor_pelagem = col16.text_input("Cor da pelagem")

        col17, col18 = st.columns(2)
        pelagem = col17.text_input("Pelagem")
        microchip = col18.text_input("Microchip")

        st.markdown("---")
        st.markdown("### Dados de Transferência")

        col19, col20 = st.columns(2)
        proprietario_contrato = col19.text_input("Proprietário que está no contrato")
        nome_transferencia = col20.text_input("Nome para transferência")

        col21, col22 = st.columns(2)
        cpf_transferencia = col21.text_input("CPF da transferência")
        email_transferencia = col22.text_input("E-mail da transferência")

        telefone_transferencia = st.text_input("Telefone da transferência")
        observacao_transferencia = st.text_area("Observação da transferência")

        st.markdown("---")
        st.markdown("### Controle Interno")

        col23, col24 = st.columns(2)
        vendedor = col23.text_input("Vendedor")
        status = col24.selectbox("Status", STATUS_OPCOES)

        observacao_interna = st.text_area("Observação interna")

        salvar = st.form_submit_button("Salvar cadastro")

        if salvar:
            if not nome_tutor:
                st.error("Preencha o nome do tutor.")
            else:
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                dados = {
                    "ID": str(uuid.uuid4())[:8],
                    "Data Cadastro": agora,
                    "Status": status,
                    "Vendedor": vendedor,
                    "Nome Tutor": nome_tutor,
                    "CPF Tutor": cpf_tutor,
                    "Telefone Tutor": telefone_tutor,
                    "Email Tutor": email_tutor,
                    "Rua Avenida": rua_av,
                    "Numero": numero,
                    "Complemento": complemento,
                    "Bairro": bairro,
                    "Cidade": cidade,
                    "Estado": estado,
                    "CEP": cep,
                    "Nome Animal": nome_animal,
                    "Data Nascimento Animal": data_nascimento.strftime("%d/%m/%Y"),
                    "Raca": raca,
                    "Sexo": sexo,
                    "Cor Pelagem": cor_pelagem,
                    "Pelagem": pelagem,
                    "Microchip": microchip,
                    "Proprietario Contrato": proprietario_contrato,
                    "Nome Transferencia": nome_transferencia,
                    "CPF Transferencia": cpf_transferencia,
                    "Email Transferencia": email_transferencia,
                    "Telefone Transferencia": telefone_transferencia,
                    "Observacao Transferencia": observacao_transferencia,
                    "Observacao Interna": observacao_interna,
                    "Data Alteracao": agora
                }

                salvar_registro(dados)
                st.success("Cadastro salvo com sucesso na planilha.")


def tela_producao():
    st.subheader("⚙️ Produção")

    df = carregar_base()

    if df.empty:
        st.info("Nenhum cadastro encontrado na planilha.")
        return

    busca = st.text_input("Buscar por Nome, CPF, Telefone ou Microchip", key="busca_producao")

    if busca:
        busca_normalizada = busca.lower().strip()
        df = df[
            df["Nome Tutor"].astype(str).str.lower().str.contains(busca_normalizada, na=False) |
            df["CPF Tutor"].astype(str).str.lower().str.contains(busca_normalizada, na=False) |
            df["Telefone Tutor"].astype(str).str.lower().str.contains(busca_normalizada, na=False) |
            df["Microchip"].astype(str).str.lower().str.contains(busca_normalizada, na=False)
        ]

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.write("")
    st.markdown("### Alterar Status")

    ids = df["ID"].astype(str).tolist()

    if not ids:
        st.warning("Nenhum registro encontrado para alterar.")
        return

    id_selecionado = st.selectbox(
        "Selecione o cadastro",
        ids,
        format_func=lambda x: f"{x} - {df[df['ID'].astype(str) == x]['Nome Tutor'].iloc[0]}"
    )

    registro = df[df["ID"].astype(str) == id_selecionado].iloc[0]
    status_atual = str(registro["Status"]).strip()

    if status_atual in STATUS_OPCOES:
        index_status = STATUS_OPCOES.index(status_atual)
    else:
        index_status = 0

    novo_status = st.selectbox(
        "Novo Status",
        STATUS_OPCOES,
        index=index_status
    )

    if st.button("Atualizar Status na Planilha"):
        sucesso = atualizar_status(id_selecionado, novo_status)

        if sucesso:
            st.success("Status atualizado com sucesso na planilha.")
            st.rerun()
        else:
            st.error("Não foi possível atualizar o status.")


def tela_dashboard():
    with st.sidebar:
        st.markdown("## 🐶 Liberty")
        st.markdown("**Pedigree**")
        st.markdown("---")

        pagina = st.radio(
            "Menu",
            ["Visão Geral", "Formulário", "Produção"]
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

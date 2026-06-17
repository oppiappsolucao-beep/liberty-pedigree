import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(
    page_title="Liberty Pedigree",
    page_icon="🐶",
    layout="wide"
)

SHEET_ID = "1qkhbn11yyaaXniRpoZd0CfG0T3LF9hJT1kRTh2foVmM"


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

    gc = gspread.authorize(credentials)

    return gc


def carregar_base():
    gc = conectar_google()

    planilha = gc.open_by_key(SHEET_ID)

    aba = planilha.worksheet("Base")

    dados = aba.get_all_records()

    return pd.DataFrame(dados)


st.title("🐶 Liberty Pedigree")

try:
    df = carregar_base()

    st.success("✅ Conectado com sucesso ao Google Sheets")

    st.metric(
        "Total de registros encontrados",
        len(df)
    )

    st.write("Prévia da base:")

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as erro:
    st.error("Erro ao conectar com a planilha")

    st.code(str(erro))

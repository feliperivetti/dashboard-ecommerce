# src/db_connection.py

import os
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env que está na raiz do projeto
# O 'find_dotenv' ajuda a localizar o .env quando o script roda de dentro de /src
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

@st.cache_resource
def get_db_engine():
    """
    Cria e retorna uma engine de conexão do SQLAlchemy para o PostgreSQL.
    Usa o cache do Streamlit para não recriar a conexão a cada interação.
    """
    try:
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        host = os.environ.get("DB_HOST")
        port = os.environ.get("DB_PORT")
        db_name = os.environ.get("DB_NAME")
        
        if not all([user, password, host, port, db_name]):
            raise ValueError("Uma ou mais variáveis de ambiente do banco não foram definidas.")

        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
        return engine
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None
import pandas as pd
import streamlit as st
from sqlalchemy import text
from sqlalchemy.engine import Engine

from db_connection import get_db_engine

@st.cache_data
def fetch_data(query: str):
    """
    Executa uma query no banco de dados e retorna o resultado como um DataFrame do Pandas.
    Usa o cache de dados do Streamlit para performance.
    """
    engine = get_db_engine()
    if engine:
        try:
            with engine.connect() as connection:
                df = pd.read_sql(text(query), connection)
            return df
        except Exception as e:
            st.error(f"Erro ao executar a query: {e}")
            return pd.DataFrame()
    return pd.DataFrame()


def get_delivery_time_distribution():
    query = """
        SELECT
            (order_delivered_customer_date::DATE - order_purchase_timestamp::DATE) AS dias_para_entrega,
            COUNT(*) AS quantidade_de_pedidos
        FROM analytics_orders
        WHERE order_delivered_customer_date IS NOT NULL 
        GROUP BY dias_para_entrega
        HAVING COUNT(*) > 100
        ORDER BY dias_para_entrega ASC;
    """
    return fetch_data(query)


def get_raw_delivery_times():
    query = """
        WITH delivery_data AS (
            SELECT
                (order_delivered_customer_date::DATE - order_purchase_timestamp::DATE) AS dias_para_entrega
            FROM
                analytics_orders
            WHERE
                order_delivered_customer_date IS NOT NULL AND
                order_purchase_timestamp IS NOT NULL
        )
        SELECT
            dias_para_entrega
        FROM
            delivery_data
        WHERE
            dias_para_entrega >= 0;
    """
    df = fetch_data(query)
    return df


def get_delivery_times_and_reviews():
    query = """
        WITH delivery_data AS (
            SELECT
                order_id,
                review_score,
                (order_delivered_customer_date::DATE - order_purchase_timestamp::DATE) AS dias_para_entrega
            FROM
                analytics_orders
            WHERE
                order_delivered_customer_date IS NOT NULL AND
                order_purchase_timestamp IS NOT NULL AND
                review_score IS NOT NULL
        )
        SELECT
            review_score,
            dias_para_entrega
        FROM
            delivery_data
        WHERE
            dias_para_entrega >= 0;
    """
    df = fetch_data(query)
    return df


def get_sales_by_dimension(dimension: str):
    # Validação simples para evitar SQL Injection
    allowed_dimensions = ['customer_city', 'customer_state', 'product_category_name']
    if dimension not in allowed_dimensions:
        st.error(f"Dimensão de análise inválida: {dimension}")
        return pd.DataFrame()

    query = f"""
        SELECT 
            {dimension},
            SUM(payment_value) as total_faturamento
        FROM 
            analytics_orders
        WHERE 
            {dimension} IS NOT NULL
        GROUP BY 
            {dimension}
        ORDER BY 
            total_faturamento DESC
        LIMIT 10; -- Pegando os 10 maiores para o gráfico não ficar poluído
    """
    return fetch_data(query)


def get_faturamento_total():
    query = """
        SELECT 
            SUM(payment_value) AS total_faturamento
        FROM 
            analytics_orders;
    """
    df = fetch_data(query)
    return df['total_faturamento'].iloc[0] if not df.empty else 0.0


def get_total_orders():
    query = """
        SELECT
            COUNT(DISTINCT order_id) AS total_orders
        FROM
            analytics_orders;
    """
    df = fetch_data(query)
    return df['total_orders'].iloc[0] if not df.empty else 0


def get_ticket_medio():
    query = """
        SELECT 
            SUM(payment_value) / COUNT(DISTINCT order_id) AS ticket_medio
        FROM 
            analytics_orders;
    """
    df = fetch_data(query)
    return df['ticket_medio'].iloc[0] if not df.empty else 0.0


def get_average_rating():
    query = """
        SELECT 
            AVG(review_score) AS average_rating
        FROM 
            analytics_orders
        WHERE 
            review_score IS NOT NULL;
    """
    df = fetch_data(query)
    return df['average_rating'].iloc[0] if not df.empty else 0.0


def get_average_delivery_time():
    query = """
        SELECT 
            AVG(order_delivered_customer_date::DATE - order_purchase_timestamp::DATE) AS average_delivery_time
        FROM 
            analytics_orders
        WHERE 
            order_delivered_customer_date IS NOT NULL;
    """
    df = fetch_data(query)
    return df['average_delivery_time'].iloc[0] if not df.empty else 0.0


def get_total_customers():
    query = """
        SELECT 
            COUNT(DISTINCT customer_unique_id) AS total_customers
        FROM 
            analytics_orders;
    """
    df = fetch_data(query)
    return df['total_customers'].iloc[0] if not df.empty else 0


def get_orders_by_time_period(start_date: str, end_date: str):
    query = f"""
        SELECT
            DATE(order_purchase_timestamp) AS date,
            SUM(price) AS total_price
        FROM
            analytics_orders
        WHERE
            order_purchase_timestamp IS NOT NULL AND
            DATE(order_purchase_timestamp) BETWEEN '{start_date}' AND '{end_date}'
        GROUP BY
            DATE(order_purchase_timestamp)
        ORDER BY
            date ASC;
    """
    df = fetch_data(query)
    return df if not df.empty else None


if __name__ == "__main__":
    print(get_orders_by_time_period('2016-09-15', '2018-08-29'))

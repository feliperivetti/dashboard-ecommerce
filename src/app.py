import streamlit as st
import queries

from components import (
    display_correlation_boxplot,
    display_delivery_time_histogram,
    kpi_card,
    display_orders_data,
    display_revenue_forecast,
    display_sales_by_category_pie_chart,
)


def main():
    # --- Configuração da Página ---
    st.set_page_config(
        layout="centered",
        page_title="Dashboard de Vendas",
        page_icon="📈"
    )

    st.title("📈 Dashboard - Análise de Vendas")

    # --- Exibe os KPIs principais ---
    kpi_card(
        faturamento_total=queries.get_faturamento_total(),
        total_pedidos=queries.get_total_orders(), 
        ticket_medio=queries.get_ticket_medio(),
        avaliacao_media=queries.get_average_rating(),
        tempo_medio_entrega=queries.get_average_delivery_time(),
        total_clientes=queries.get_total_customers(),
    )

    # --- Criação das Abas ---
    tab1, tab2, tab3 = st.tabs(["📊 Análise de Vendas", "🚚 Análise de Entregas", "🔮 Previsão do Faturamento"])

    # --- Conteúdo da Aba 1: Análise de Vendas ---
    with tab1:
        st.header("Visão Geral das Vendas")
        display_orders_data()
        display_sales_by_category_pie_chart()
        
    # --- Conteúdo da Aba 2: Análise de Entregas ---
    with tab2:
        st.header("Performance da Logística e Satisfação do Cliente")
        display_delivery_time_histogram()
        display_correlation_boxplot()
    
    # --- Conteúdo da Aba 3: Previsão ---
    with tab3:
        display_revenue_forecast()


if __name__ == "__main__":
    main()

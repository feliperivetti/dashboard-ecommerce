import streamlit as st
import components, queries


def main():
    # --- Configuração da Página ---
    st.set_page_config(
        layout="centered",
        page_title="Dashboard de Vendas",
        page_icon="📈"
    )

    st.title("📈 Dashboard - Análise de Vendas")

    # --- Exibe os KPIs principais ---
    components.card_kpi(
        faturamento_total=queries.get_faturamento_total(),
        total_pedidos=queries.get_total_orders(), 
        ticket_medio=queries.get_ticket_medio(),
        avaliacao_media=queries.get_average_rating(),
        tempo_medio_entrega=queries.get_average_delivery_time(),
        total_clientes=queries.get_total_customers(),
    )

    # --- Criação das Abas ---
    # Vamos criar duas abas, uma para cada contexto de análise
    tab1, tab2 = st.tabs(["📊 Análise de Vendas", "🚚 Análise de Entregas"])

    # --- Conteúdo da Aba 1: Análise de Vendas ---
    with tab1:
        st.header("Visão Geral das Vendas")

        components.display_orders_analysis()

        components.display_sales_by_category_pie_chart()
        

    # --- Conteúdo da Aba 2: Análise de Entregas ---
    with tab2:
        st.header("Performance da Logística e Satisfação do Cliente")

        # Análise de Tempo de Entrega (Histograma)
        components.display_delivery_time_histogram()

        # Análise de Correlação: Tempo de Entrega vs. Avaliação
        components.display_correlation_boxplot()
    
    
    # # --- Conteúdo da Aba 4: Previsão ---
    # with tab3:
    #     # Componente de previsão de faturamento
    #     components.display_revenue_forecast()

    # --- Conteúdo da Aba 3: Análise Geográfica ---
    # with tab4:
    #     # Mapa interativo que criamos
    #     components.display_customer_map_by_city()


if __name__ == "__main__":
    main()




# # --- Exibe os KPIs principais ---
#     components.card_kpi(
#         faturamento_total=queries.get_faturamento_total(),
#         total_pedidos=queries.get_total_orders(), 
#         ticket_medio=queries.get_ticket_medio(),
#         avaliacao_media=queries.get_average_rating(),
#         tempo_medio_entrega=queries.get_average_delivery_time(),
#         total_clientes=queries.get_total_customers(),
#     )
#     st.write("---")
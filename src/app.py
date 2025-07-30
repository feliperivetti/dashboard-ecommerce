import streamlit as st
import components, queries


def main():
    # Configuração da página
    st.set_page_config(layout="centered", page_title="Dashboard de Vendas", page_icon=":bar_chart:")

    st.title("Dashboard de Análise de Vendas")

    # --- Exibe os KPIs principais ---
    components.card_kpi(
        faturamento_total=queries.get_faturamento_total(),
        total_pedidos=queries.get_total_orders(), 
        ticket_medio=queries.get_ticket_medio(),
        avaliacao_media=queries.get_average_rating(),
        tempo_medio_entrega=queries.get_average_delivery_time(),
        total_clientes=queries.get_total_customers(),
    )
    st.write("---")

    # --- Análise de Vendas por Cidade, Estado ou Setor ---
    components.display_sales_by_category_pie_chart()
    st.write("---")

    # --- Análise de Vendas por Período ---
    components.display_orders_analysis()
    st.write("---")

    # --- Análise de Tempo de Entrega ---
    components.display_delivery_time_histogram()


if __name__ == "__main__":
    main()

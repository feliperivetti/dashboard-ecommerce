from datetime import date
import streamlit as st

from .. import queries


def display_orders_data():
    with st.container(border=True):
        st.markdown("#### Análise de Vendas por Período")

        # 1. Define o intervalo possível para o slider dinamicamente
        min_date = date(2016, 9, 15)
        max_date = date(2018, 8, 29)

        # 2. Cria o slider de intervalo de datas
        start_date, end_date = st.slider(
            "Selecione o intervalo de datas para a análise",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="DD/MM/YYYY",
        )
        
        # 3. Exibe o período selecionado
        # st.write(f"Analisando dados de **{start_date.strftime('%d/%m/%Y')}** até **{end_date.strftime('%d/%m/%Y')}**")

        # 4. Busca e exibe os dados do período
        if start_date > end_date:
            st.error("Erro: A data de início não pode ser posterior à data de fim.")
        else:
            # Chama a função de consulta passando as datas do slider
            df_orders = queries.get_orders_by_time_period(start_date, end_date)
            
            if not df_orders.empty:
                chart_data = df_orders.set_index('date')
                st.line_chart(chart_data)
            else:
                st.warning("Nenhum pedido encontrado para o período selecionado.")

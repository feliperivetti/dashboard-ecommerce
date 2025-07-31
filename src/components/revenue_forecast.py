from datetime import date
from prophet.plot import plot_plotly, plot_components_plotly
import streamlit as st

import forecasting
import queries


def display_revenue_forecast():
    with st.container(border=True):
        st.markdown("#### Prevendo e Identificando Tendências no Faturamento")

        days_to_forecast = st.number_input(
            "Selecione o número de dias para a previsão futura:",
            min_value=30, max_value=365, value=90, step=30
        )

        # 1. Define o intervalo possível para o slider dinamicamente
        min_date = date(2016, 9, 15)
        max_date = date(2018, 8, 29)

        # 2. Cria o slider de intervalo de datas
        start_date, end_date = st.slider(
            "Selecione o intervalo de datas para treinar o modelo de previsão",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="DD/MM/YYYY",
        )

        if start_date > end_date:
            st.error("Erro: A data de início não pode ser posterior à data de fim.")
        else:
            ...

        # Selecionar o intervalo de datas para treinamento do modelo
        st.markdown(f"**Período de Treinamento:** {start_date} até {end_date}")
        # st.date_input()

        df_revenue = queries.get_orders_by_time_period(start_date, end_date)
        
        if df_revenue.empty:
            st.warning("Não foi possível carregar os dados de faturamento para a previsão.")
            return

        df_prophet = df_revenue.rename(columns={'date': 'ds', 'total_price': 'y'})

        # --- MUDANÇA AQUI ---
        # A chamada agora é para a função no módulo 'forecasting'
        with st.spinner(f"Treinando modelo e prevendo os próximos {days_to_forecast} dias..."):
            model, forecast = forecasting.train_and_forecast_model(df_prophet, days_to_forecast)

        # A parte de visualização continua a mesma
        st.subheader(f"Previsão do Faturamento para os Próximos {days_to_forecast} Dias",
                    help="O gráfico mostra o faturamento histórico (pontos azuis), a previsão do modelo (linha azul) e o intervalo de confiança (área azul clara).")
        
        # Gera a figura do Plotly como antes
        fig1 = plot_plotly(model, forecast)
        fig1.data[0].marker.color = '#87CEEB'

        fig1.update_layout(
            title=f"Previsão de Faturamento para os Próximos {days_to_forecast} Dias",
            xaxis_title="Data",
            yaxis_title="Faturamento (R$)"
        )
        st.plotly_chart(fig1, use_container_width=True, theme="streamlit")

        st.subheader("Componentes da Previsão")
        st.info("Abaixo estão as tendências e sazonalidades que o modelo identificou.")
        
        fig2 = plot_components_plotly(model, forecast)
        st.plotly_chart(fig2, use_container_width=True, theme="streamlit")

        # --- NOVA SEÇÃO: AVALIAÇÃO DO MODELO ---
        st.write("---")
        st.subheader("Qualidade da Previsão (Acurácia do Modelo)")
        st.info("Clique no botão para executar a validação cruzada. Este processo simula previsões no passado para estimar o erro médio do modelo. Pode levar alguns minutos.")

        if st.button("Calcular Métricas de Acurácia"):
            df_revenue = queries.get_orders_by_time_period(min_date, max_date)
            df_prophet = df_revenue.rename(columns={'date': 'ds', 'total_price': 'y'})
            
            with st.spinner("Executando validação cruzada... Por favor, aguarde."):
                # Chama a nova função de avaliação
                df_metrics = forecasting.evaluate_model(df_prophet)
                        
            st.write("Métricas de Performance (Horizonte de 90 dias):")

            # Mostra as principais métricas. 'mape' e 'mae' são as mais fáceis de interpretar.
            st.dataframe(df_metrics[['horizon', 'mape', 'mae', 'rmse']].head())
            # st.dataframe(df_metrics.head())

            # Explicação das Métricas
            st.write("#### O que essas métricas significam?")
            mape_value = df_metrics['mape'].iloc[0] * 100
            mae_value = df_metrics['mae'].iloc[0]
            st.markdown(f"""
            - **MAPE (Mean Absolute Percentage Error):** Em média, o erro da nossa previsão é de **{mape_value:.2f}%**. É a medida de erro relativo.
            - **MAE (Mean Absolute Error):** Em média, o erro da nossa previsão é de **R$ {mae_value:,.2f}**. É o erro absoluto médio na mesma unidade do faturamento.
            """)

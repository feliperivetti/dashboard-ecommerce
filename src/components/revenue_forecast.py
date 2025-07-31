from datetime import date
from prophet.plot import plot_plotly, plot_components_plotly
import streamlit as st

import forecasting
import queries


def _generate_and_plot_forecast(df_prophet, days_to_forecast):
    """
    Recebe dados preparados, treina o modelo, e retorna as figuras dos gráficos.
    Esta função isola a lógica de modelagem e plotagem.
    """
    try:
        with st.spinner(f"Treinando modelo e prevendo os próximos {days_to_forecast} dias..."):
            model, forecast = forecasting.train_and_forecast_model(df_prophet, days_to_forecast)

        # Gráfico 1: Previsão Principal
        fig1 = plot_plotly(model, forecast)
        fig1.data[0].marker.color = '#87CEEB'
        fig1.update_layout(
            title=f"Previsão para os Próximos {days_to_forecast} Dias",
            xaxis_title="Data",
            yaxis_title="Faturamento (R$)"
        )

        # Gráfico 2: Componentes da Previsão
        fig2 = plot_components_plotly(model, forecast)
        fig2.update_layout(title_text="Componentes da Previsão (Tendência e Sazonalidade)")
        
        return fig1, fig2

    except Exception as e:
        st.error(f"Ocorreu um erro ao gerar a previsão: {e}")
        st.warning("Isso geralmente acontece se o período de treinamento selecionado for muito curto. Tente selecionar um intervalo de datas maior.")
        return None, None


def _render_accuracy_section(queries, forecasting, min_date, max_date):
    with st.container(border=True):
        st.subheader("Qualidade do Modelo de Referência")
        st.info("As métricas abaixo são calculadas usando o histórico completo de dados para uma avaliação robusta do modelo.")

        if st.button("Calcular Métricas de Acurácia"):
            with st.spinner("Executando validação cruzada... Isso pode levar alguns minutos."):
                try:
                    full_history_df = queries.get_orders_by_time_period(min_date, max_date)
                    df_full_prophet = full_history_df.rename(columns={'date': 'ds', 'total_price': 'y'})
                    
                    df_metrics = forecasting.evaluate_model(df_full_prophet)
                    
                    st.write("Métricas de Performance (Horizonte de 60 dias):")
                    st.dataframe(df_metrics[['horizon', 'mape', 'mae', 'rmse']].head())
                    
                    mape_value = df_metrics['mape'].iloc[0] * 100
                    mae_value = df_metrics['mae'].iloc[0]
                    st.markdown(f"""
                    - **MAPE:** Em média, o erro da previsão é de **{mape_value:.2f}%**.
                    - **MAE:** Em média, o erro da previsão é de **R$ {mae_value:,.2f}**.
                    """)
                except ValueError as e:
                    st.error(f"Erro na Validação: {e}")
                    st.warning("O histórico de dados pode ser muito curto para os parâmetros de validação. Verifique a função 'evaluate_model' em forecasting.py.")
                except Exception as e:
                    st.error(f"Ocorreu um erro inesperado durante a validação: {e}")


def display_revenue_forecast():
    with st.container(border=True):
        st.markdown("#### Prevendo e Identificando Tendências no Faturamento")
        
        # --- CONTROLES DE VOLTA À PÁGINA PRINCIPAL ---
        days_to_forecast = st.number_input(
            "Selecione o número de dias para a previsão futura:",
            min_value=30, max_value=365, value=60, step=30
        )

        min_date = date(2016, 9, 15)
        max_date = date(2018, 8, 29)

        start_date, end_date = st.slider(
            "Selecione o intervalo de datas para treinar o modelo:",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="DD/MM/YYYY"
        )
        st.markdown(f"**Período de Treinamento Selecionado:** `{start_date}` até `{end_date}`")

        if start_date > end_date:
            st.error("Erro: A data de início não pode ser posterior à data de fim.")
            return

        # Busca os dados para o período de treino selecionado
        df_revenue = queries.get_orders_by_time_period(start_date, end_date)
        
        if df_revenue.empty:
            st.warning("Nenhum dado de faturamento encontrado no período selecionado.")
            return

        df_prophet = df_revenue.rename(columns={'date': 'ds', 'total_price': 'y'})
        
        fig_forecast, fig_components = _generate_and_plot_forecast(df_prophet, days_to_forecast)

        if fig_forecast and fig_components:
            st.plotly_chart(fig_forecast, use_container_width=True, theme="streamlit")
            st.plotly_chart(fig_components, use_container_width=True, theme="streamlit")

        # --- Seção de Avaliação do Modelo ---
        _render_accuracy_section(queries, forecasting, min_date, max_date)

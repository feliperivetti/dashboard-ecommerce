from prophet.plot import plot_plotly, plot_components_plotly
import streamlit as st

from .. import forecasting, queries


def display_revenue_forecast():
    """
    Exibe a seção de previsão de faturamento.
    A lógica de UI fica aqui, a lógica de modelagem fica no forecasting.py.
    """
    st.header("🔮 Previsão de Faturamento")

    days_to_forecast = st.number_input(
        "Selecione o número de dias para a previsão futura:",
        min_value=30, max_value=365, value=90, step=30
    )

    min_date = "2016-09-15"
    max_date = "2018-08-29"

    # Selecionar o intervalo de datas para treinamento do modelo
    st.markdown(f"**Período de Treinamento:** {min_date} até {max_date}")

    df_revenue = queries.get_orders_by_time_period(min_date, max_date)
    
    if df_revenue.empty:
        st.warning("Não foi possível carregar os dados de faturamento para a previsão.")
        return

    df_prophet = df_revenue.rename(columns={'date': 'ds', 'total_price': 'y'})

    # --- MUDANÇA AQUI ---
    # A chamada agora é para a função no módulo 'forecasting'
    with st.spinner(f"Treinando modelo e prevendo os próximos {days_to_forecast} dias..."):
        model, forecast = forecasting.train_and_forecast_model(df_prophet, days_to_forecast)

    st.success("Previsão concluída!")

    # A parte de visualização continua a mesma
    st.subheader("Gráfico de Previsão")
    st.info("O gráfico mostra o faturamento histórico (pontos pretos), a previsão do modelo (linha azul) e o intervalo de confiança (área azul clara).")
    
    fig1 = plot_plotly(model, forecast)
    fig1.update_layout(
        title=f"Previsão de Faturamento para os Próximos {days_to_forecast} Dias",
        xaxis_title="Data",
        yaxis_title="Faturamento (R$)"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Componentes da Previsão")
    st.info("Abaixo estão as tendências e sazonalidades que o modelo identificou nos dados. Isso ajuda a entender o comportamento do seu faturamento.")
    
    fig2 = plot_components_plotly(model, forecast)
    st.plotly_chart(fig2, use_container_width=True)

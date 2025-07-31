import pandas as pd
from prophet import Prophet
import streamlit as st


@st.cache_data
def train_and_forecast_model(df: pd.DataFrame, periods: int):
    """
    Recebe um DataFrame, treina o modelo Prophet e retorna o modelo e a previsão.

    Args:
        df (pd.DataFrame): DataFrame preparado com as colunas 'ds' e 'y'.
        periods (int): Número de dias para prever no futuro.

    Returns:
        tuple: Uma tupla contendo o modelo treinado e o DataFrame da previsão.
    """
    # Instancia o modelo com sazonalidades padrão
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    
    # Treina o modelo com os dados
    model.fit(df)
    
    # Cria um DataFrame com as datas futuras
    future = model.make_future_dataframe(periods=periods)
    
    # Gera a previsão
    forecast = model.predict(future)
    
    return model, forecast

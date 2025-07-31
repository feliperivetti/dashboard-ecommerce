import pandas as pd
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
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


def evaluate_model(df: pd.DataFrame):
    """
    Executa a validação cruzada no modelo e retorna as métricas de performance.

    Args:
        df (pd.DataFrame): DataFrame com as colunas 'ds' e 'y'.

    Returns:
        pd.DataFrame: Um DataFrame contendo diversas métricas de erro.
    """
    # Configuração da validação cruzada
    # initial: período inicial de treino
    # period: a cada quantos dias faremos um novo "corte" de treino
    # horizon: quantos dias à frente queremos prever em cada corte
    df_cv = cross_validation(
        model=Prophet().fit(df),
        initial='360 days',
        period='30 days',
        horizon='60 days',
        parallel="processes"
        # initial=f'{len(df)} days',
        # period=f'{horizon//2} days'
        # horizon=f'{horizon} days',
    )
    
    df_performance = performance_metrics(df_cv)
    
    return df_performance

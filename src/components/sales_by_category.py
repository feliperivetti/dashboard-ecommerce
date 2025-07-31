import streamlit as st
import plotly.express as px

from .. import queries


def display_sales_by_category_pie_chart():
    with st.container(border=True):
        st.markdown("#### Análise de Faturamento por Categoria")

        # Dicionário que mapeia o nome amigável para a coluna do banco de dados
        categories = {
            "Estado": "customer_state",
            "Cidade": "customer_city",
            "Setor de Produto": "product_category_name"
        }

        # Seletor para o usuário escolher a métrica
        selected_category = st.selectbox(
            "Selecione a métrica para a análise de faturamento:",
            options=list(categories.keys()) # Usa as chaves do dicionário como opções
        )
        
        # Busca o nome da coluna correspondente à seleção
        column_to_query = categories[selected_category]

        # Chama a função de consulta com a coluna dinâmica
        df_dimension = queries.get_sales_by_dimension(column_to_query)

        # Verifica se a consulta retornou dados
        if not df_dimension.empty:
            st.write(f"#### Distribuição de Faturamento por **{selected_category}**.")
            
            # Cria a figura do gráfico de pizza com Plotly
            fig_pie = px.pie(
                df_dimension, 
                values='total_faturamento', 
                names=column_to_query,
                color_discrete_sequence=px.colors.sequential.Blues_r # Paleta de cores
            )
            
            # Exibe o gráfico no Streamlit
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            # Mensagem de aviso dinâmica
            st.warning(f"Não foram encontrados dados de vendas por {selected_category}.")

import streamlit as st
import plotly.express as px

from .. import queries


def display_correlation_boxplot():
    with st.container(border=True):
        st.markdown("#### Tempo de Entrega vs. Avaliação do Cliente", help="O gráfico abaixo mostra a distribuição do tempo de entrega para cada nota de avaliação. Se as caixas para notas baixas (1, 2) estiverem mais altas, significa que entregas mais longas recebem piores avaliações.")
        
        df_corr = queries.get_delivery_times_and_reviews()
        
        if not df_corr.empty:
            # Para o Box Plot, é melhor tratar a nota como uma categoria
            df_corr['review_score'] = df_corr['review_score'].astype(str)

            # Remove outliers de entrega para uma melhor visualização do box plot
            cutoff = df_corr['dias_para_entrega'].quantile(0.95) # Remove os 5% mais longos
            df_filtered = df_corr[df_corr['dias_para_entrega'] <= cutoff]

            fig = px.box(
                df_filtered,
                x='review_score',
                y='dias_para_entrega',
                color='review_score',
                labels={
                    "review_score": "Avaliação do Cliente ⭐",
                    "dias_para_entrega": "Tempo de Entrega (dias)"
                },
                # Ordena o eixo X de 1 a 5
                category_orders={"review_score": ["1", "2", "3", "4", "5"]}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não foi possível carregar os dados para a análise de correlação.")

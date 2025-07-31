import streamlit as st
import plotly.express as px

import queries


def display_delivery_time_histogram():
    with st.container(border=True):
        st.markdown("#### Distribuição do Tempo de Entrega", help="Para uma melhor visualização, os valores 1% mais altos foram removidos.")
        
        df_delivery_raw = queries.get_raw_delivery_times()
        
        if not df_delivery_raw.empty:        
            # 2. Calcula o limite para considerar um valor como outlier (99º percentil)
            # Isso significa que estamos removendo o 1% dos maiores valores.
            cutoff = df_delivery_raw['dias_para_entrega'].quantile(0.99)
            
            # 3. Filtra o DataFrame para remover os outliers
            df_filtered = df_delivery_raw[df_delivery_raw['dias_para_entrega'] <= cutoff]
            
            fig = px.histogram(
                df_filtered, 
                x="dias_para_entrega",
                nbins=50,
            )
            
            # Ajusta os nomes dos eixos para maior clareza
            fig.update_layout(
                xaxis_title="Tempo de Entrega (dias)",
                yaxis_title="Número de Pedidos (Frequência)"
            )
            
            # 5. Exibe o gráfico no Streamlit
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não foi possível carregar os dados de tempo de entrega.")

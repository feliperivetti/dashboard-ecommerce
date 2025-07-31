from datetime import date
import plotly.express as px
import streamlit as st
import queries


def card_kpi(faturamento_total, total_pedidos, ticket_medio, avaliacao_media, tempo_medio_entrega, total_clientes):
    with st.container(border=True):
        # TÍTULO CENTRALIZADO USANDO MARKDOWN E HTML
        # st.markdown("<h3 style='text-align: center;'>Métricas Principais</h3>", unsafe_allow_html=True)
        st.markdown("## Principais Métricas")
        # Organizando os 6 KPIs em um grid de 3 linhas e 2 colunas
        
        # --- Primeira linha ---
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="💰 Faturamento Total", value=f"R$ {faturamento_total:,.2f}")
        with col2:
            st.metric(label="📦 Total de Pedidos", value=f"{total_pedidos:,}")

        # --- Segunda linha ---
        col3, col4 = st.columns(2)
        with col3:
            st.metric(label="🛒 Ticket Médio", value=f"R$ {ticket_medio:,.2f}")
        with col4:
            st.metric(label="⭐ Avaliação Média", value=f"{avaliacao_media:.2f}")
        
        # --- Terceira linha ---
        col5, col6 = st.columns(2)
        with col5:
            st.metric(label="🚚 Tempo Médio de Entrega", value=f"{tempo_medio_entrega:.1f} dias")
        
        # Só exibe o sexto KPI se a coluna 'customer_id' existir
        if total_clientes is not None:
            with col6:
                st.metric(label="👥 Clientes Únicos", value=f"{total_clientes:,}")


def display_orders_analysis():
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

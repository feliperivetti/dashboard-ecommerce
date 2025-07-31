import streamlit as st


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

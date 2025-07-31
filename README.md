# 📈 Dashboard de Análise de Vendas E-commerce

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B)](https://streamlit.io)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75)](https://plotly.com/)
[![Prophet](https://img.shields.io/badge/Prophet-1.1%2B-0072B2)](https://facebook.github.io/prophet/)

Este projeto é um dashboard interativo e completo para análise de dados de um e-commerce, construído com Streamlit. Ele transforma dados brutos de vendas em insights acionáveis, permitindo uma visão 360° do negócio, desde KPIs de alto nível até análises preditivas de faturamento.

---

## 🚀 Demonstração Ao Vivo

### [Clique aqui para ver o dashboard em ação!](URL_DO_SEU_APP_NO_STREAMLIT_CLOUD)

*(Substitua a URL acima pelo link do seu aplicativo após o deploy)*

---

## ✨ Funcionalidades Principais

O dashboard é organizado em abas para uma navegação intuitiva e focada:

###  KPIs de Alto Nível
- **Visão Imediata:** Um card no topo da página exibe as métricas mais importantes do negócio em tempo real:
  - 💰 **Faturamento Total**
  - 📦 **Total de Pedidos**
  - 🛒 **Ticket Médio**
  - ⭐ **Avaliação Média dos Clientes**
  - 🚚 **Tempo Médio de Entrega**
  - 👥 **Total de Clientes Únicos**

### 📊 Aba: Análise de Vendas
- **Performance de Vendas no Tempo:** Um gráfico de barras interativo com um slider de datas que permite ao usuário explorar o volume de vendas para qualquer período desejado.
- **Faturamento por Categoria:** Um gráfico de pizza dinâmico que mostra a distribuição de faturamento por **Estado**, **Cidade** ou **Setor de Produto**. As categorias menores são agrupadas de forma inteligente em "Outros" para uma visualização mais limpa.

### 🚚 Aba: Análise de Entregas
- **Distribuição do Tempo de Entrega:** Um histograma que revela quantos dias os pedidos geralmente levam para serem entregues, com um filtro automático de outliers para focar na distribuição principal.
- **Análise de Correlação 🔗:** Um gráfico de Box Plot que responde a uma pergunta de negócio crucial: **"Pedidos que demoram mais para chegar realmente recebem avaliações piores?"**.

### 🔮 Aba: Previsão de Faturamento
- **Laboratório de Previsão:** Uma seção avançada que utiliza o modelo **Prophet (do Facebook/Meta)** para prever o faturamento futuro.
  - **Interatividade Total:** O usuário pode definir o número de dias para a previsão.
  - **Gráficos Detalhados:** Exibe não apenas a previsão, mas também os seus componentes: tendência de crescimento, sazonalidade anual e sazonalidade semanal.
  - **Métricas de Acurácia:** Permite calcular métricas de erro do modelo (**MAPE** e **MAE**) através de validação cruzada para entender a confiabilidade da previsão.

---

## 🗃️ Dados e Metodologia ELT

### Fonte dos Dados
Os dados utilizados neste projeto são públicos e foram obtidos através da plataforma Kaggle. Eles representam um conjunto de dados de e-commerce anonimizado e rico em informações.
- **Dataset:** [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### Processo de Dados (ELT)
A preparação dos dados seguiu uma abordagem de **ELT (Extract, Load, Transform)**, otimizando o processamento dentro do banco de dados:

1.  **`[E]` Extract:** Os arquivos `.csv` originais foram extraídos do Kaggle.
2.  **`[L]` Load:** Cada arquivo foi carregado como uma tabela "crua" (raw) no banco de dados PostgreSQL, sem transformações iniciais.
3.  **`[T]` Transform:** Utilizando o poder do próprio PostgreSQL, foram executadas consultas SQL para limpar, juntar, tratar tipos e modelar os dados, criando a tabela analítica final (`analytics_orders`) que alimenta o dashboard de forma eficiente.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Dashboard:** Streamlit
* **Banco de Dados:** PostgreSQL
* **Manipulação de Dados:** Pandas
* **Visualização de Dados:** Plotly Express
* **Previsão de Séries Temporais:** Prophet

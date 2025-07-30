import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# --- 1. CONFIGURAÇÕES GLOBAIS ---

# Carregando variáveis de ambiente do arquivo .env
load_dotenv()

# Lembre-se: em um projeto real, use variáveis de ambiente!
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "olist_db")

# É uma boa prática verificar se a senha foi carregada
if not DB_PASSWORD:
    raise ValueError("Senha do banco de dados não encontrada! Verifique seu arquivo .env")

DATA_PATH = "data/"


def create_db_engine(user, password, host, port, db_name) -> Engine | None:
    try:
        connection_str = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        engine = create_engine(connection_str)
        print("Conexão com o PostgreSQL bem-sucedida!")
        return engine
    except Exception as e:
        print(f"Erro ao criar a engine de conexão: {e}")
        return None


def load_raw_data(engine: Engine, data_path: str) -> None:
    files_to_load = {
        'olist_orders_dataset.csv': 'orders',
        'olist_order_items_dataset.csv': 'order_items',
        'olist_customers_dataset.csv': 'customers',
        'olist_products_dataset.csv': 'products',
        'olist_order_payments_dataset.csv': 'order_payments',
        'olist_order_reviews_dataset.csv': 'order_reviews',
        'product_category_name_translation.csv': 'category_name_translation'
    }

    print("\nIniciando carregamento dos dados brutos (Etapa de Staging)...")

    for filename, tablename in files_to_load.items():
        try:
            file_path = os.path.join(data_path, filename)
            df = pd.read_csv(file_path)
            df.to_sql(tablename, engine, if_exists='replace', index=False)
            print(f"  - Tabela '{tablename}' carregada com {len(df)} linhas.")
        except FileNotFoundError:
            print(f"  - ERRO: Arquivo '{filename}' não encontrado. Pulando.")
        except Exception as e:
            print(f"  - ERRO ao carregar a tabela '{tablename}': {e}")


def transform_data(engine: Engine) -> None:
    create_analytics_table_query = """
    DROP TABLE IF EXISTS analytics_orders;
    CREATE TABLE analytics_orders AS
    SELECT
        o.order_id,
        c.customer_unique_id,
        c.customer_city,
        c.customer_state,
        oi.order_item_id,
        p.product_category_name,
        cat.product_category_name_english AS product_category,
        oi.price,
        oi.freight_value,
        op.payment_type,
        op.payment_installments,
        op.payment_value,
        r.review_score,
        o.order_status,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date
    FROM
        orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN category_name_translation cat ON p.product_category_name = cat.product_category_name
    LEFT JOIN order_payments op ON o.order_id = op.order_id
    LEFT JOIN order_reviews r ON o.order_id = r.order_id
    WHERE 
        o.order_status = 'delivered';
    """

    print("\nIniciando transformação dos dados (Criando Tabela de Análise)...")
    try:
        with engine.connect() as connection:
            connection.execute(text(create_analytics_table_query))
            connection.commit()
        print("Tabela 'analytics_orders' criada com sucesso!")
    except Exception as e:
        print(f"ERRO ao criar a tabela de análise: {e}")


def main():
    """
    Função principal que orquestra todo o processo de ETL.
    """
    print("--- Iniciando Pipeline de Processamento de Dados da Olist ---")
    
    # 1. Cria a conexão com o banco
    engine = create_db_engine(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    if engine:
        # 2. Carrega os dados brutos
        load_raw_data(engine, DATA_PATH)

        # 3. Transforma os dados
        transform_data(engine)

        # 4. Verifica o resultado
        print("\n--- Verificação Final ---")
        try:
            df_final = pd.read_sql("SELECT * FROM analytics_orders LIMIT 5", engine)
            print("Amostra da tabela final 'analytics_orders':")
            print(df_final)
        except Exception as e:
            print(f"ERRO ao buscar dados da tabela de análise: {e}")
            
    print("\n--- Pipeline Finalizado ---")


if __name__ == "__main__":
    main()

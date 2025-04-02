from db.db_connection import get_db_connection

# Buscar lista de clientes com meta_account_id no banco de dados
def get_clients():
    """Retorna uma lista de clientes ativos com Meta Ads Account ID."""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, meta_account_id FROM clientes WHERE meta_account_id IS NOT NULL")
            clients = cur.fetchall()  # Lista de tuplas (id, meta_account_id)
        conn.close()
        return clients
    except Exception as e:
        print(f"Erro ao buscar clientes: {e}")
        return []
    
# Inserir dados no banco de dados com executemany
def insert_meta_ads_data(client_id, data, start_date, end_date):
    """Insere os dados extraídos no banco de dados usando executemany para eficiência."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            query = """
                INSERT INTO meta_ads_data (cliente_id, data_inicio, data_fim, campaign_id, campaign_name, 
                                          impressions, clicks, ctr, cpc, cpm, spend, leads, cpl)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = [(client_id, start_date, end_date) + entry for entry in data]
            
            cur.executemany(query, values)  # Inserindo múltiplos registros de uma vez
        conn.commit()
        print(f"Dados inseridos com sucesso para o cliente {client_id}.")
    except Exception as e:
        print(f"Erro ao inserir dados no banco: {e}")
    finally:
        conn.close()
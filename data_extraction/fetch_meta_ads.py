import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime
from db_connection import get_db_connection  # Importando a conexão separada
from config.settings import META_ACCESS_TOKEN, META_API_VERSION


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

# Função para buscar dados do Meta Ads
def fetch_meta_ads_data(meta_account_id, start_date, end_date):
    """Faz requisição à API do Meta Ads e retorna os dados extraídos."""
    url = f"https://graph.facebook.com/{META_API_VERSION}/act_{meta_account_id}/insights"

    params = {
        "access_token": META_ACCESS_TOKEN,
        "time_range": f"{{'since':'{start_date}','until':'{end_date}'}}",
        "level": "account",
        "fields": "impressions,clicks,ctr,cpc,cpm,spend,actions",
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print(f"Erro na requisição: {data['error']['message']}")
            return None

        extracted_data = []
        for item in data.get("data", []):
            impressions = int(item.get("impressions", 0))
            clicks = int(item.get("clicks", 0))
            ctr = float(item.get("ctr", 0))
            cpc = float(item.get("cpc", 0))
            cpm = float(item.get("cpm", 0))
            spend = float(item.get("spend", 0))

            # Leads e CPL são obtidos da chave "actions"
            actions = item.get("actions", [])
            leads = next((int(a["value"]) for a in actions if a["action_type"] == "lead"), 0)
            cpl = spend / leads if leads > 0 else 0  # Custo por Lead

            extracted_data.append((
                impressions, clicks, ctr, cpc, cpm, spend, leads, cpl
            ))

        return extracted_data

    except Exception as e:
        print(f"Erro ao buscar dados do Meta Ads: {e}")
        return None

# Inserir dados no banco de dados com executemany
def insert_meta_ads_data(client_id, data, start_date, end_date):
    """Insere os dados extraídos no banco de dados usando executemany para eficiência."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            query = """
                INSERT INTO meta_ads_data (cliente_id, data_inicio, data_fim, 
                                          impressions, clicks, ctr, cpc, cpm, spend, leads, cpl)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = [(client_id, start_date, end_date) + entry for entry in data]
            
            cur.executemany(query, values)  # Inserindo múltiplos registros de uma vez
        conn.commit()
        print(f"Dados inseridos com sucesso para o cliente {client_id}.")
    except Exception as e:
        print(f"Erro ao inserir dados no banco: {e}")
    finally:
        conn.close()

# Função principal
def main(data_inicial="2025-01-01", data_final=None):
    print("Buscando dados do Meta Ads...")

    start_date = data_inicial
    if data_final is None:
        end_date = datetime.today().strftime("%Y-%m-%d")
    else:
        end_date = data_final

    clients = get_clients()
    if not clients:
        print("Nenhum cliente encontrado com meta_account_id.")
        return

    for client_id, meta_account_id in clients:
        print(f"Buscando dados para Cliente ID: {client_id} | Meta Account ID: {meta_account_id}...")
        data = fetch_meta_ads_data(meta_account_id, start_date, end_date)
        if data:
            insert_meta_ads_data(client_id, data, start_date, end_date)
        else:
            print(f"Nenhum dado encontrado para Cliente {client_id}.")

if __name__ == "__main__":
    main()

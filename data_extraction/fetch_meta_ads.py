import requests
from database.db_connection import get_db_connection

# Configurações da API
ACCESS_TOKEN = "SEU_ACCESS_TOKEN"
AD_ACCOUNT_ID = "SEU_AD_ACCOUNT_ID"
API_VERSION = "v16.0"
URL = f"https://graph.facebook.com/{API_VERSION}/act_{AD_ACCOUNT_ID}/insights"

def fetch_meta_ads_data():
    """Busca os dados de campanhas no Meta Ads."""
    params = {
        "access_token": ACCESS_TOKEN,
        "fields": "impressions,clicks,ctr,cpc,cpm,spend,conversions,roas,leads,cpl",
        "time_range": {"since": "2025-03-01", "until": "2025-03-15"}
    }
    
    response = requests.get(URL, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Erro ao buscar dados: {response.text}")
        return []

def save_to_database(data):
    """Salva os dados no PostgreSQL."""
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    
    for entry in data:
        cursor.execute("""
            INSERT INTO meta_ads_data (impressions, clicks, ctr, cpc, cpm, gasto, conversoes, roas, leads, cpl)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            entry['impressions'], entry['clicks'], entry['ctr'],
            entry['cpc'], entry['cpm'], entry['spend'], 
            entry['conversions'], entry['roas'], entry['leads'], entry['cpl']
        ))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("Buscando dados do Meta Ads...")
    data = fetch_meta_ads_data()
    print("Salvando no banco de dados...")
    save_to_database(data)
    print("Processo concluído!")

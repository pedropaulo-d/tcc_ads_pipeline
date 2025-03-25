import requests
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from datetime import datetime, timedelta
from config.settings import META_ACCESS_TOKEN, META_AD_ACCOUNT_ID

def fetch_meta_ads_data(start_date=None, end_date=None):
    """ Obtém os dados do Meta Ads para o período especificado """
    print("Buscando dados do Meta Ads...")

    # Se não passar datas, pega os últimos 7 dias
    if not start_date or not end_date:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=7)

    # Converter strings para objetos datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Formatar corretamente para a API do Meta Ads
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    print(f"Buscando dados de {start_date} até {end_date}...")

    url = f"https://graph.facebook.com/v22.0/act_{META_AD_ACCOUNT_ID}/insights"
    
    params = {
        "access_token": META_ACCESS_TOKEN,
        "fields": "impressions,clicks,ctr,cpc,cpm,spend,actions",
        "time_range": json.dumps({"since": start_date, "until": end_date})
    }

    try:
        response = requests.get(url, params=params)
        response_data = response.json()

        if "error" in response_data:
            print(f"Erro na requisição: {response_data['error']['message']}")
            return []

        data = response_data.get("data", [])

        extracted_data = []
        for insights in data:
            spend = float(insights.get("spend", 0))  # Gasto total
            leads = 0
            
            # Busca os Leads dentro da lista "actions"
            for action in insights.get("actions", []):
                if action["action_type"] == "lead":
                    leads = int(action["value"])
                    break
            
            # Calcula o CPL (Custo por Lead)
            cpl = round(spend / leads, 2) if leads > 0 else None  

            extracted_data.append({
                "impressions": int(insights.get("impressions", 0)),
                "clicks": int(insights.get("clicks", 0)),
                "ctr": float(insights.get("ctr", 0)),
                "cpc": float(insights.get("cpc", 0)),
                "cpm": float(insights.get("cpm", 0)),
                "spend": spend,
                "leads": leads,
                "cpl": cpl
            })

        print("Dados extraídos com sucesso!")
        return extracted_data

    except Exception as e:
        print(f"Erro ao buscar dados do Meta Ads: {e}")
        return []

# Teste rápido
if __name__ == "__main__":
    data = fetch_meta_ads_data("2025-01-01", "2025-03-25")
    print(json.dumps(data, indent=4))

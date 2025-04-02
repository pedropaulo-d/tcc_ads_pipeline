import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.settings import META_ACCESS_TOKEN, META_API_VERSION

# Função para buscar dados do Meta Ads
def fetch_meta_ads_data(meta_account_id, start_date, end_date):
    """Faz requisição à API do Meta Ads e retorna os dados extraídos."""
    url = f"https://graph.facebook.com/{META_API_VERSION}/act_{meta_account_id}/insights"

    params = {
        "access_token": META_ACCESS_TOKEN,
        "time_range": f"{{'since':'{start_date}','until':'{end_date}'}}",
        "level": "campaign",
        "fields": "campaign_id,campaign_name,impressions,clicks,ctr,cpc,cpm,spend,actions",
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print(f"Erro na requisição: {data['error']['message']}")
            return None

        extracted_data = []
        for item in data.get("data", []):
            campaign_id = str(item.get("campaign_id", None))
            campaign_name = str(item.get("campaign_name", None))
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
                campaign_id, campaign_name, impressions, clicks, ctr, cpc, cpm, spend, leads, cpl
            ))

        return extracted_data

    except Exception as e:
        print(f"Erro ao buscar dados do Meta Ads: {e}")
        return None

from datetime import datetime
from db.db_operations import get_clients, insert_meta_ads_data
from meta_ads.fetch_data import fetch_meta_ads_data

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
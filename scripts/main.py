import requests
import mysql.connector
import matplotlib.pyplot as plt

# 1. Função para buscar dados da poha da API do Meta Ads
def fetch_meta_ads_data():
    # Exemplo de requisição (substitua pelos dados reais da sua conta e tokens)
    url = "https://graph.facebook.com/v16.0/act_<ad_account_id>/insights"
    params = {
        "access_token": "<seu_token>",
        "fields": "impressions,clicks,spend",
        "time_range": {"since": "2025-03-01", "until": "2025-03-15"}
    }
    response = requests.get(url, params=params)
    return response.json().get('data', [])

# 2. Função para inserir dados no banco do MySQL
def save_to_database(data, table_name):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="<sua_senha>",
        database="relatorios_ads"
    )
    cursor = db.cursor()

    # Cria a tabela se não existir
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            impressions INT,
            clicks INT,
            spend FLOAT
        )
    """)

    # Inserir os dados aqui mesmo
    for entry in data:
        cursor.execute(f"""
            INSERT INTO {table_name} (impressions, clicks, spend)
            VALUES (%s, %s, %s)
        """, (entry['impressions'], entry['clicks'], entry['spend']))
    
    db.commit()
    cursor.close()
    db.close()

# 3. função pra criar visualização com o Matplotlib
def create_visualization():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="<sua_senha>",
        database="relatorios_ads"
    )
    cursor = db.cursor()
    cursor.execute("SELECT impressions, clicks FROM meta_ads")
    data = cursor.fetchall()
    cursor.close()
    db.close()

    impressions = [row[0] for row in data]
    clicks = [row[1] for row in data]

    # Grafico (meio baum ja)
    plt.bar(range(len(impressions)), impressions, label="Impressions")
    plt.plot(range(len(clicks)), clicks, color="red", label="Clicks")
    plt.legend()
    plt.title("Relatório Meta Ads")
    plt.xlabel("Campanhas")
    plt.ylabel("Quantidade")
    plt.show()

# 4. Pipeline dos crias
if __name__ == "__main__":
    print("Buscando dados do Meta Ads...")
    meta_data = fetch_meta_ads_data()
    print("Salvando dados no banco de dados...")
    save_to_database(meta_data, "meta_ads")
    print("Criando visualização...")
    create_visualization()
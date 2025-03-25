import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Configurações do Banco de Dados
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "traq_data"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "minha_senha_segura")
}

# Configurações do Meta Ads
META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "seu_token_aqui")
META_AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID", "seu_ad_account_id")
META_API_VERSION = os.getenv("META_API_VERSION", "v22.0")
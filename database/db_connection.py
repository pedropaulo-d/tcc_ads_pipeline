import psycopg2
from config.settings import DB_CONFIG
def get_db_connection():
    """Cria e retorna uma conexão com o PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            database=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )

        return conn
    
    except Exception as e:
        print(f'Erro ao conectar ao banco de dados: {e}')
        return None
    
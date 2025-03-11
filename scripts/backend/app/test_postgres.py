import psycopg2
from app.config import Config

# teste de conexão com o banco
DATABASE_URL = Config.DATABASE_URL

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")

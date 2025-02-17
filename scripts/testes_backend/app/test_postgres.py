import psycopg2

# Configuração do banco
DATABASE_URL = "postgresql://tcc_user:senha123@localhost/tcc_db_teste"

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")

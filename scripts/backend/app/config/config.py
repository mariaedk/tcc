import os
from dotenv import load_dotenv

# automaticamente procura por um arquivo chamado ".env" na raiz do projeto
load_dotenv()

# armazena o valor da variavel definida no .env
class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")

import os
from dotenv import load_dotenv

# automaticamente procupra por um arquivo chamado .env na raiz do projeto
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")

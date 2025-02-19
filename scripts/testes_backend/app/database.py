from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import Config

# importa a URL do banco pra criar a conexão com o banco de dados
engine = create_engine(Config.DATABASE_URL)

# sessão para interagir com o banco.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# classe base criada pelo sqlalchemy. serve como fundamento para criação
# de outros modelos no banco de dados
# ao herdar de Base, será convertida automaticamente em uma tabela no PostgreSQL
Base = declarative_base()

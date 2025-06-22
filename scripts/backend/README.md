# Backend - API REST

Este serviço é a API do sistema, responsável por processar, armazenar e disponibilizar os dados recebidos dos dispositivos de campo. A aplicação é desenvolvida em Python com o framework FastAPI e adota autenticação, organização modular e versionamento de banco de dados.
## Funcionalidades
```
    Recebimento de dados de medições em lote via JSON

    Armazenamento em banco de dados relacional (MariaDB)

    Autenticação baseada em JWT

    Exportação de relatórios (PDF, Excel)

    Endpoints para sensores, dispositivos, medições, unidades e usuários

    Suporte a filtros por período e tipo 
```

## Tecnologias Utilizadas
```
    FastAPI (framework principal)

    SQLAlchemy + Alembic (ORM e versionamento do banco)

    Pydantic (validação e tipagem)

    Uvicorn (ASGI server)

    WeasyPrint (geração de relatórios em PDF)

    OpenPyXL e Pandas (exportação para Excel)
```

## Instalação
* Pré-requisitos:
```
    Python 3.11+

    Banco de dados (MariaDB)
```

* Passos

1. Clone o repositório: git clone https://github.com/mariaedk/tcc.git

2. Instale as dependências:

```pip install -r requirements.txt```

3. Configure o ambiente:
Crie um arquivo .env com as variáveis:
``` 
DB_URL=mysql+pymysql://usuario:senha@localhost:3306/nome_db
SECRET_KEY=suachavesecreta
JWT_EXPIRE_MINUTES=60 
```

4. Rode as migrações do banco:

alembic upgrade head

Inicie o servidor:
```
uvicorn app.main:app --reload
```
Estrutura do Projeto

    schemas/: Schemas de entrada/saída (Pydantic)

    models/: Modelos ORM (SQLAlchemy)

    routes/: Rotas da API

    services/: Lógica de negócios

    alembic/: Migrações de banco de dados

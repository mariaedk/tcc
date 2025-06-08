# Importador Firebird -> API TCC

Este projeto realiza a importação de dados de um banco de dados Firebird (`.FDB`) e publica as informações em uma API (FastAPI) hospedada na AWS.

## Funcionalidades

- Leitura de dados históricos do banco Firebird.
- Publicação dos dados em lote na API REST.
- Controle de autenticação com token JWT.
- Log de erros e acompanhamento da execução.

## Tecnologias utilizadas

- Python 3.10+
- Firebird
- FastAPI (para destino dos dados)
- Bibliotecas: `fdb`, `requests`, `tqdm`, `python-dotenv`


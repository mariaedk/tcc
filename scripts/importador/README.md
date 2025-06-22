# Importador Firebird

Este script realiza a importação automatizada de dados de vazão de um banco Firebird (.FDB) e publica essas informações em lote em uma API REST desenvolvida com FastAPI. É utilizado no contexto de um sistema de monitoramento de Estações de Tratamento de Água (ETA).
## Funcionalidades
```
    Leitura dos dados históricos (vazão ETA1 e ETA2) a partir de Firebird

    Autenticação com a API via JWT

    Envio em lotes para o endpoint "/coletas/batch"

    Registro de logs (importador_fdb.log)

    Configuração totalmente parametrizável via .env
```
## Tecnologias Utilizadas
```
    Python 3.10+

    Firebird 2.x

    FastAPI (API de destino)

    Bibliotecas: fdb, requests, tqdm, python-dotenv
```
## Instalação

1. Clone o repositório: git clone https://github.com/mariaedk/tcc.git

2. Instale as dependências:

```pip install -r requirements.txt```

3. Crie um arquivo .env com as seguintes variáveis:
```
    FIREBIRD_PATH=localhost:/caminho/para/arquivo.FDB
    FIREBIRD_USER=sysdba
    FIREBIRD_PASSWORD=masterkey

    API_URL=http://localhost:8000/coletas
    AUTH_URL=http://localhost:8000/usuarios/login
    USERNAME=admin
    PASSWORD=admin123

    SENSOR_VAZAO1_ID=1
    SENSOR_VAZAO2_ID=2
    UNIDADE_ID=1
    TIPO_MEDICAO=INST
    BATCH_SIZE=500
```

4. Para executar o script:

```python importador.py```

## Durante a execução:
```
    Os dados da tabela HISTINFO são lidos.

    Os registros são organizados no formato JSON esperado pela API.

    O envio ocorre em lotes de tamanho configurável (BATCH_SIZE).

    Falhas são registradas no log, incluindo datas inválidas e erros de autenticação.
```
## Log
```
Os eventos são registrados no arquivo importador_fdb.log, incluindo:

    Obtenção do token

    Erros HTTP

    Quantidade de registros enviados por lote
```
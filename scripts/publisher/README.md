# Publicador OPC UA

Este serviço conecta-se a um CLP via protocolo OPC UA, realiza leituras das variáveis expostas no CLP a cada 3 minutos e publica os dados em lote no broker MQTT ao final de cada hora cheia. É utilizado para alimentar o pipeline de monitoramento de dados ambientais em Estações de Tratamento de Água (ETA).
### Funcionalidades
```
    Conecta-se ao CLP via OPC UA com autenticação

    Realiza leitura periódica (a cada 3 minutos)

    Armazena os dados em lote na memória

    Publica um batch com todas as leituras da hora no tópico MQTT configurado

    Reestabelece conexões automaticamente em caso de falhas

    Gera logs de operação detalhados
```
### Tecnologias Utilizadas
```
    asyncua: Conexão assíncrona com servidores OPC UA

    paho-mqtt: Cliente MQTT

    python-dotenv: Carregamento de variáveis de ambiente

    asyncio, json, logging: Módulos padrão Python
```
### Instalação

1. Clone o repositório: git clone https://github.com/mariaedk/tcc.git

2. Instale as dependências: ```pip install -r requirements.txt```

3. Configure o arquivo .env com os seguintes parâmetros:
```
    OPC_URL=opc.tcp://192.168.0.100:4840
    OPC_USERNAME=usuario_opc
    OPC_PW=senha_opc

    MQTT_BROKER=broker.hivemq.com
    MQTT_PORT=1883
    MQTT_TOPIC=eta/dados

    MQTT_USERNAME=usuario_mqtt
    MQTT_PASSWORD=senha_mqtt
```

4. Execute o script principal: ``` python publicador_batch_single_read.py```

### Formato do Batch Publicado

Ao final de cada hora, o serviço publica um JSON com este formato:
```
[
  {
    "timestamp": "2025-06-22T14:03:00",
    "valores": {
      "VAZAO_SAIDA1": 64.2,
      "VAZAO_SAIDA2": 66.1
    },
    "falha": false
  },
  ...
]
```
### Logs

Todos os eventos (conexão, leitura, publicação e erros) são registrados no arquivo leitura_batch_hora.log.
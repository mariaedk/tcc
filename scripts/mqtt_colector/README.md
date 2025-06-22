# Coletor MQTT

Este serviço escuta tópicos MQTT publicados pelo Raspberry Pi e envia os dados de medições para a API REST.
## Funcionalidades
```
    Escuta tópicos MQTT definidos via .env

    Autentica na API FastAPI utilizando JWT

    Converte payloads MQTT em estrutura compatível com o endpoint /coletas

    Publica os dados automaticamente após validação

    Mantém registros detalhados de operação via log
```

## Tecnologias Utilizadas
```
    Python 3.10+

    MQTT com paho-mqtt

    API REST com autenticação JWT

    Bibliotecas: requests, dotenv, json, logging
```
## Instalação

1. Clone o repositório: git clone https://github.com/mariaedk/tcc.git

2. Instale as dependências: ```pip install -r requirements.txt```

3. Crie um arquivo .env com os parâmetros (exemplo):
```
    USERNAME=admin
    PASSWORD=admin123

    MQTT_BROKER=broker.hivemq.com
    MQTT_PORT=1883
    MQTT_TOPIC=eta/dados

    MQTT_USERNAME=usuario_mqtt
    MQTT_PASSWORD=senha_mqtt

    AUTH_URL=http://localhost:8000/usuarios/login
    COLETA_URL=http://localhost:8000/coletas

    # Mapeamento lógico
```

4. Para rodar o coletor manualmente: ```python collector_mqtt.py```

### Formato Esperado do Payload MQTT

O payload recebido deve ser um JSON no formato:
```
{
  "timestamp": "2025-06-22T15:00:00Z",
  "valores": {
    "VAZAO_SAIDA1": 65.3,
    "VAZAO_SAIDA2": 67.1
  },
  "falha": false
}
```
### Log

As mensagens e erros são registrados no arquivo mqtt_coletor.log.
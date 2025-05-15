# Projeto: Coletor MQTT para API FastAPI

Este serviço escuta mensagens publicadas em um tópico MQTT (por exemplo, por um Raspberry Pi), extrai os dados de medições e envia para uma API FastAPI hospedada na mesma instância ou rede.

## Requisitos

- Python 3.10 ou superior
- API FastAPI rodando e acessível (ex: `http://localhost:8000`)
- Broker MQTT acessível e configurado corretamente
- Arquivo `.env` ou `config.py` com as seguintes constantes:
  - `MQTT_BROKER`, `MQTT_PORT`, `MQTT_TOPIC`
  - `AUTH_URL`, `COLETA_URL`, `USERNAME`, `PASSWORD`
  - `SENSOR_MAP`, `UNIDADE_MAP`

## Instalação

```bash
sudo apt update
sudo apt install python3-pip -y
pip install -r requirements.txt
Execução manual

python3 collector_mqtt.py
```

## Configurando como serviço (systemd)

Copie o arquivo de serviço para o systemd:

```sudo cp mqtt_consumer.service /etc/systemd/system/```

Ative e inicie o serviço:

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable mqtt_consumer
sudo systemctl start mqtt_consumer
```

Verifique o status:

```sudo systemctl status mqtt_consumer```

## Logs

mqtt_coletor.log → registra mensagens de conexão, autenticação, envio e erros durante a execução.

## Estrutura esperada das mensagens MQTT

```bash
{
  "tipo": "hora",
  "dados": [
    {
      "tipo_sensor": "VAZAO",
      "media_valor": 20.1,
      "data": "2025-05-07T20:00:00",
      "falha": false
    },
    ...
  ]
}
```

## Estrutura dos dados enviados para a API

```bash
{
  "origem": "CLP",
  "medicoes": [
    {
      "sensor_id": 1,
      "unidade_id": 1,
      "valor": 20.1,
      "valor_str": null,
      "valor_bool": null,
      "data_hora": "2025-05-07T20:00:00",
      "falha": false,
      "tipo": "hora"
    }
  ]
}
```
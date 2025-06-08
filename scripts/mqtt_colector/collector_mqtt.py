import json
import requests
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
from config import (
    MQTT_BROKER, MQTT_PORT, MQTT_TOPIC,
    AUTH_URL, COLETA_URL, USERNAME, PASSWORD,
    SENSOR_MAP, UNIDADE_MAP, MQTT_USERNAME, MQTT_PASSWORD
)

import logging

logging.basicConfig(
    filename="mqtt_coletor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

token_data = {
    "token": None,
    "expires_at": None
}

def authenticate():
    try:
        response = requests.post(AUTH_URL, data={
            "username": USERNAME,
            "password": PASSWORD
        })
        response.raise_for_status()
        data = response.json()
        token_data["token"] = data["access_token"]
        token_data["expires_at"] = datetime.utcnow() + timedelta(minutes=59)
        logging.info("Token obtido com sucesso")
    except Exception as e:
        logging.error(f"Erro ao autenticar: {str(e)}")
        token_data["token"] = None

def is_token_valid():
    return token_data["token"] and token_data["expires_at"] > datetime.utcnow()

# conexão mqtt
def on_connect(client, userdata, flags, rc):
    logging.info(f"Conectado ao broker MQTT com código {rc}")
    client.subscribe(MQTT_TOPIC)

# ao receber mensagem
def on_message(client, userdata, msg):
    if not is_token_valid():
        authenticate()
    if not token_data["token"]:
        logging.warning("Sem token válido")
        return

    try:
        payload = json.loads(msg.payload.decode()) # carregar o payload que recebeu no broker
        logging.info(f"Payload recebido: {payload}")

        if isinstance(payload, dict):
            payloads = [payload]
        elif isinstance(payload, list):
            payloads = payload
        else:
            logging.error(f"Formato de payload inválido: {type(payload)}")
            return

        medicoes = []

        for item in payloads:
            timestamp = item.get("timestamp")
            falha = item.get("falha", False)
            valores = item.get("valores", {})

            for tipo_sensor, valor in valores.items():
                sensor_id = SENSOR_MAP.get(tipo_sensor)
                unidade_id = UNIDADE_MAP.get(tipo_sensor)

                if sensor_id is None or unidade_id is None:
                    logging.warning(f"Sensor {tipo_sensor} não mapeado.")
                    continue

                medicao = {
                    "sensor_id": sensor_id,
                    "unidade_id": unidade_id,
                    "valor": valor,
                    "valor_str": None,
                    "valor_bool": None,
                    "data_hora": timestamp,
                    "falha": falha,
                    "tipo": "INST"
                }

                medicoes.append(medicao)

        if medicoes:
            headers = {"Authorization": f"Bearer {token_data['token']}"}
            coleta = {
                "origem": "CLP",
                "data_hora": medicoes[0]["data_hora"] if medicoes else None,
                "medicoes": medicoes
            }

            try:
                response = requests.post(COLETA_URL, json=coleta, headers=headers)
                response.raise_for_status()
                logging.info(f"Coleta enviada com sucesso - Status {response.status_code}")
            except Exception as e:
                logging.error(f"Erro ao enviar coleta: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    logging.error(f"Resposta da API: {e.response.text}")
        else:
            logging.warning("Nenhuma medição válida montada.")

    except Exception as e:
        logging.error(f"Erro ao processar mensagem MQTT: {str(e)}")

def main():
    authenticate()
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()


import json
import time
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
    """
    Realiza a autenticação na API para obter um token JWT.

    Envia um POST com as credenciais e armazena o token e seu tempo de expiração
    na estrutura 'token_data'. Caso haja erro, o token armazenado será 'None'.
    """
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
    """
    Verifica se o token atual é válido com base na expiração.

    Retorna:
        bool: True se o token existe e ainda está dentro da validade.
    """
    return token_data["token"] and token_data["expires_at"] > datetime.utcnow()

def on_connect(client, userdata, flags, rc):
    """
    Callback executado ao conectar no broker MQTT.

    Assina o tópico configurado para começar a receber mensagens.
    """
    logging.info(f"Conectado ao broker MQTT com código {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    """
    Callback executado ao receber uma mensagem MQTT.

    - Valida e renova o token de autenticação se necessário;
    - Decodifica o payload JSON;
    - Mapeia os dados recebidos em medições;
    - Envia as medições à API se forem válidas.
    """
    if not is_token_valid():
        authenticate()
    if not token_data["token"]:
        logging.warning("Sem token válido. Ignorando mensagem.")
        return

    try:
        payload = json.loads(msg.payload.decode())
        logging.info(f"Payload recebido: {payload}")

        tipo = payload.get("tipo")
        dados = payload.get("dados", [])

        medicoes = []
        for item in dados:

            tipo_sensor = item.get("tipo_sensor")
            sensor_id = SENSOR_MAP.get(tipo_sensor)
            unidade_id = UNIDADE_MAP.get(tipo_sensor)
            if unidade_id is None:
                logging.warning(f"Tipo de sensor {tipo_sensor} não mapeado.")
                continue

            medicao = {
                "sensor_id": sensor_id,
                "unidade_id": unidade_id,
                "valor": item.get("media_valor"),
                "valor_str": None,
                "valor_bool": None,
                "data_hora": item.get("data"),
                "falha": item.get("falha", False),
                "tipo": tipo
            }

            medicoes.append(medicao)

        if medicoes:
            headers = {"Authorization": f"Bearer {token_data['token']}"}
            coleta = {
                "origem": "CLP",
                "medicoes": medicoes
            }
            response = requests.post(COLETA_URL, json=coleta, headers=headers)
            logging.info(f"Coleta enviada com sucesso - Status {response.status_code}")
        else:
            logging.warning("Nenhuma medição válida foi montada.")

    except Exception as e:
        logging.error(f"Erro ao processar mensagem MQTT: {str(e)}")

def main():
    """
    Função principal do script.

    - Autentica com a API;
    - Conecta ao broker MQTT;
    - Inicia o loop para escutar mensagens indefinidamente.
    """
    authenticate()
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()


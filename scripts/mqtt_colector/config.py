from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

AUTH_URL = os.getenv("AUTH_URL")
COLETA_URL = os.getenv("COLETA_URL")


SENSOR_MAP = {
    "VAZAO_SAIDA1": 1,  
    "VAZAO_SAIDA2": 2
}

UNIDADE_MAP = {
    "VAZAO_SAIDA1": 5,
    "VAZAO_SAIDA2": 5
}

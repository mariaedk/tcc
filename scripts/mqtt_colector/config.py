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
    "vazao_entrada": 1,  
    "vazao_saida": 2,
    "nivel": 3      
}

UNIDADE_MAP = {
    "vazao_entrada": 1,  # L/s
    "vazao_saida": 1,
    "nivel": 3,          # Litros
    "bomba_ativa": 2,    # Status
    "status": 4,         # Texto
}

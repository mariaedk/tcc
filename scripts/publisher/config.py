from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

OPC_URL = os.getenv("OPC_URL")
OPC_USERNAME = os.getenv("OPC_USERNAME")
OPC_PW = os.getenv("OPC_PW")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

TIPO_DISPOSITIVO_PADRAO = "CLP"
NODE_HORARIO = "ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.horario_leitura"

SENSORES = {
    "VAZAO_SAIDA1": "ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.vazao_saida1",
    "VAZAO_SAIDA2": "ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.vazao_saida2"
}

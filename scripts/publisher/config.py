from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

OPC_URL = os.getenv("OPC_URL")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

TIPO_DISPOSITIVO_PADRAO = "CLP"

NODES = {
    "vazao_entrada": r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.vazao_entrada",
    "vazao_saida":   r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.vazao_saida",
    "nivel":         r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.nivel_reservatorio",
    "bomba_ativa":   r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.bomba_ativa",
    "status":        r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.status_coleta",
    "hora":          r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.horario_leitura",
}

SENSORES = {
    "vazao_entrada": r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.vazao_entrada",
    "vazao_saida":   r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.vazao_saida",
    "nivel":         r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.nivel_reservatorio"
}

TIPO_AGRUPAMENTO_HORA = "HORA"
TIPO_AGRUPAMENTO_DIA = "DIA"

OPC_URL = "opc.tcp://192.168.119.204:4840"
MQTT_BROKER = "15.229.109.126"
MQTT_PORT = 1883
MQTT_TOPIC = "tcc/monitoramento"

NODES = {
    "vazao_entrada": r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.vazao_entrada",
    "vazao_saida":   r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.vazao_saida",
    "nivel":         r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.nivel_reservatorio",
    "bomba_ativa":   r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.bomba_ativa",
    "status":        r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.status_coleta",
    "hora":          r"ns=4;s=|var|Plc3 V3.5.19.61-77f4 192.168.119.204 .Application.GVL.horario_leitura",
}

# MQTT
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "tcc/monitoramento"

# API
AUTH_URL = "http://localhost:8000/auth/login"
MEDICAO_URL = "http://localhost:8000/medicao"

# CREDENCIAIS
USERNAME = "maria"
PASSWORD = "maria123"
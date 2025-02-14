import paho.mqtt.client as mqtt
import json
import time
from config import BROKER, PORT, TOPIC  # Importa variáveis do arquivo config.py

# Configurar o cliente MQTT
client = mqtt.Client()
client.connect(BROKER, PORT, 60)

# Publicar mensagens continuamente
while True:
    dados = {
        "temperatura": 3,
        "pressao": 1
    }
    client.publish(TOPIC, json.dumps(dados))
    print(f"Mensagem publicada: {dados}")
    time.sleep(2)

import paho.mqtt.client as mqtt
from config import BROKER, PORT, TOPIC  # Importa variáveis do arquivo config.py

# Callback para quando uma mensagem é recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

# Configurar cliente MQTT
client = mqtt.Client()
client.on_message = on_message

# Conectar ao broker e subscrever ao tópico
client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

print("Subscrevendo ao tópico... Aguardando mensagens...")

# Manter conexão ativa
client.loop_forever()

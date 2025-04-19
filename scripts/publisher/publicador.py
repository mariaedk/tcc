import asyncio
from asyncua import Client
from datetime import datetime
import json
import logging
import paho.mqtt.client as mqtt
from config import OPC_URL, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, NODES
from paho.mqtt.client import CallbackAPIVersion

# criar um logger para guardar as informações de erro/gravações
logging.basicConfig(
    filename="leitura_clp_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

mqtt_client = mqtt.Client()

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    logging.info("conectado ao broker MQTT da AWS")
except Exception as e:
    logging.error(f"erro ao conectar no broker da AWS: {str(e)}")
    raise

async def main():
    client = Client(url=OPC_URL)

    try:
        # na URL definida pro protocolo OPC UA no clp (ip do clp + porta opc ua), realiza a conexão
        await client.connect()
        logging.info("conectado ao clp")

        # fica em loop lendo os valores das variáveis.
        while True:
            payload = {"timestamp": datetime.now().isoformat()}
            # NODES tem os nodeIds de cada variável disponível no CLP
            for nome, node_id in NODES.items():
                try:
                    # percorre cada variável e lê o valor, monta um dicionário chamado payload.
                    node = client.get_node(node_id)
                    valor = await node.read_value()
                    payload[nome] = valor
                except Exception as e:
                    logging.error(f"Erro ao ler o node '{nome}' (ID: {node_id}): {str(e)}")
                    payload[nome] = f"erro: {e}"
            
            # via mqtt, publica os dados no tópico
            try:
                mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
                logging.info(f"Publicado no MQTT: {json.dumps(payload)}")
            except Exception as e:
                logging.error(f"Erro ao publicar via MQTT: {str(e)}")
            
            # repete o processo de leitura a cada 10segundos
            await asyncio.sleep(10)

    finally:
        await client.disconnect()
        print("desconectado do CLP")

if __name__ == "__main__":
    asyncio.run(main())

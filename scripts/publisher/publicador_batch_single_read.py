import asyncio
from asyncua import Client
from datetime import datetime
import json
import logging
import paho.mqtt.client as mqtt
from config import OPC_URL, OPC_USERNAME, OPC_PW, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, SENSORES
from config import MQTT_USERNAME, MQTT_PASSWORD

INTERVALO_SEGUNDOS = 180  # leitura a cada 3 minutos

# configuracao de logs da aplicação
logging.basicConfig(
    filename="leitura_batch_hora.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# configuracao MQTT
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.loop_start()

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    logging.info(f"Conectado ao broker MQTT {MQTT_BROKER}")
except Exception as e:
    logging.error(f"Erro ao conectar no broker: {str(e)}")
    raise


# função para garantir conexao mqtt
def garantir_conexao_mqtt():
    if not mqtt_client.is_connected():
        try:
            mqtt_client.reconnect()
            logging.info("Reconectado ao broker MQTT")
        except Exception as e:
            logging.error(f"Erro ao reconectar: {str(e)}")


# função para calcular a chave de hora para publicação
def get_hora_key():
    agora = datetime.now()
    return agora.strftime("%Y-%m-%dT%H:00:00") 


# funcao principal de leitura e publicação
async def ler_e_publicar():
    batch = []  # lista de leituras acumuladas
    hora_atual = get_hora_key()  # inicializa com a hora atual

    while True:
        client = Client(url=OPC_URL)
        client.set_user(OPC_USERNAME)
        client.set_password(OPC_PW)

        try:
            await client.connect()
            logging.info("Conectado ao CLP")

            while True:
                try:
                    timestamp = datetime.now().replace(second=0, microsecond=0).isoformat()

                    leitura = {
                        "timestamp": timestamp,
                        "valores": {},
                        "falha": False
                    }

                    for nome, node_id in SENSORES.items():
                        try:
                            node = client.get_node(node_id)
                            valor = await node.read_value()

                            if isinstance(valor, (float, int)):
                                leitura["valores"][nome.upper()] = float(valor)
                                logging.info(f"Leitura adicionada: {valor}")
                            else:
                                leitura["valores"][nome.upper()] = 0.0
                                leitura["falha"] = True
                                logging.warning(f"Leitura inválida de {nome}: {valor}")
                        except Exception as e:
                            leitura["valores"][nome.upper()] = 0.0
                            leitura["falha"] = True
                            logging.error(f"Erro ao ler node {nome}: {e}")

                    batch.append(leitura)  # adiciona no batch

                    # verifica se mudou a hora
                    hora_atual_nova = get_hora_key()

                    if hora_atual_nova != hora_atual:
                        garantir_conexao_mqtt()
                        try:
                            payload = json.dumps(batch)
                            result = mqtt_client.publish(MQTT_TOPIC, payload)
                            result.wait_for_publish()

                            if result.rc != 0:
                                logging.error(f"Erro ao publicar batch no tópico {MQTT_TOPIC}: código {result.rc}")
                            else:
                                logging.info(f"Batch publicado com {len(batch)} leituras | Hora: {hora_atual}")

                        except Exception as e:
                            logging.error(f"Erro ao publicar no MQTT: {str(e)}")

                        # limpa batch e atualiza hora
                        batch.clear()
                        hora_atual = hora_atual_nova

                    await asyncio.sleep(INTERVALO_SEGUNDOS)

                except Exception as e:
                    logging.error(f"Erro na leitura: {str(e)}")
                    break

        except Exception as e:
            logging.error(f"Erro ao conectar ao CLP: {str(e)}")

        finally:
            try:
                await client.disconnect()
                logging.info("Desconectado do CLP")
            except:
                pass

        logging.info("Tentando reconectar novamente em 5 segundos")
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(ler_e_publicar())

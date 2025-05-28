
import asyncio
from asyncua import Client
from datetime import datetime, timedelta
import json
import logging
import paho.mqtt.client as mqtt
from collections import defaultdict
from config import OPC_URL, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, SENSORES, TIPO_DISPOSITIVO_PADRAO, TIPO_AGRUPAMENTO_HORA, TIPO_AGRUPAMENTO_DIA
from config import MQTT_USERNAME, MQTT_PASSWORD

INTERVALO_SEGUNDOS = 180

logging.basicConfig(
    filename="leitura_clp_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.loop_start()

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    logging.info("Conectado ao broker MQTT "+ MQTT_BROKER)
except Exception as e:
    logging.error(f"Erro ao conectar no broker: {str(e)}")
    raise

buffer_horario = []
buffer_diario = []
ultima_hora_processada = None
ultimo_dia_processado = None

async def ler_clp(client):
    # realiza leitura dos sensores via OPC UA
    leitura = {
        "timestamp": datetime.now().isoformat(),
        "valores": {},
        "falha": False
    }

    for nome, node_id in SENSORES.items():
        try:
            node = client.get_node(node_id)
            valor = await node.read_value()
            if isinstance(valor, (float, int)):
                leitura["valores"][nome.upper()] = float(valor)
            else:
                leitura["valores"][nome.upper()] = 0.0
                leitura["falha"] = True
                logging.warning(f"Leitura inválida (não numérica) de {nome}: {valor}")
        except Exception as e:
            leitura["valores"][nome.upper()] = 0.0
            leitura["falha"] = True
            logging.error(f"Erro ao ler node {nome}: {e}")

    return leitura

def agrupar_e_publicar(registros, tipo):
    # agrupa leituras por hora ou dia e calcula média
    agrupado = defaultdict(list)

    for r in registros:
        ts = datetime.fromisoformat(r["timestamp"])
        chave = ts.replace(minute=0, second=0, microsecond=0) if tipo == TIPO_AGRUPAMENTO_HORA else ts.replace(hour=0, minute=0, second=0, microsecond=0)

        for tipo_sensor, valor in r["valores"].items():
            agrupado[(chave.isoformat(), tipo_sensor)].append({
                "valor": valor,
                "falha": r["falha"]
            })

    resultado = []
    for (data, tipo_sensor), vlist in agrupado.items():
        valores = [v["valor"] for v in vlist]
        houve_falha = any(v["falha"] for v in vlist)
        media = sum(valores) / len(valores)
        resultado.append({
            "data": data,
            "tipo_sensor": tipo_sensor,
            "media_valor": media,
            "falha": houve_falha,
            "dispositivo": TIPO_DISPOSITIVO_PADRAO
        })
    return resultado

def garantir_conexao_mqtt():
    # tenta reconectar ao broker mqtt caso desconectado
    if not mqtt_client.is_connected():
        try:
            mqtt_client.reconnect()
            logging.info("Reconectado ao broker MQTT com sucesso")
        except Exception as e:
            logging.error(f"Falha ao reconectar ao broker MQTT: {str(e)}")

# adiciona a leitura tanto no buffer horário quanto no diário
# isso permite que cada um use seu próprio conjunto de dados
def processar_leitura(leitura):
    # adiciona leitura nos dois buffers
    buffer_horario.append(leitura)
    buffer_diario.append(leitura)
    logging.info(f"Leitura adicionada: {leitura}")

# verifica se já passou uma nova hora desde a última hora processada
# se sim, agrupa as leituras dessa hora, calcula média e publica no broker MQTT
def verificar_e_publicar_hora(hora_atual):
    global buffer_horario, ultima_hora_processada

    if ultima_hora_processada is None:
        ultima_hora_processada = hora_atual - timedelta(hours=1)

    if hora_atual > ultima_hora_processada:
        registros_hora = [
            r for r in buffer_horario
            if datetime.fromisoformat(r["timestamp"]).replace(minute=0, second=0, microsecond=0) == ultima_hora_processada
        ]

        logging.info(f"Encontrado {len(registros_hora)} registros para a hora {ultima_hora_processada}")

        por_hora = agrupar_e_publicar(registros_hora, tipo=TIPO_AGRUPAMENTO_HORA)
        payload = {"tipo": TIPO_AGRUPAMENTO_HORA, "dados": por_hora}
        garantir_conexao_mqtt()
        try:
            result = mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
            result.wait_for_publish()
            if result.rc != 0:
                logging.error(f"Erro ao publicar no tópico {MQTT_TOPIC}: código {result.rc}")
            else:
                logging.info(f"Publicação bem-sucedida no tópico {MQTT_TOPIC}")
                logging.info(f"Publicado {len(por_hora)} registros por hora para {ultima_hora_processada} UKR")
        except Exception as e:
            logging.error(f"Exceção ao tentar publicar: {str(e)}")

        # avança a referência da hora
        ultima_hora_processada += timedelta(hours=1)

        # limpa os dados processados, mantendo as leituras da hora atual e futuras
        buffer_horario = [
            r for r in buffer_horario
            if datetime.fromisoformat(r["timestamp"]).replace(minute=0, second=0, microsecond=0) >= ultima_hora_processada
        ]


# verifica se o dia atual é diferente do último dia processado
# se sim, calcula a média diária com os dados acumulados e publica no broker
def verificar_e_publicar_dia(dia_atual):
    global buffer_diario, ultimo_dia_processado

    if ultimo_dia_processado is None:
        ultimo_dia_processado = dia_atual

    if dia_atual > ultimo_dia_processado:
        registros_dia = [
            r for r in buffer_diario
            if datetime.fromisoformat(r["timestamp"]).replace(hour=0, minute=0, second=0, microsecond=0) == ultimo_dia_processado
        ]
        por_dia = agrupar_e_publicar(registros_dia, tipo=TIPO_AGRUPAMENTO_DIA)
        payload = {"tipo": TIPO_AGRUPAMENTO_DIA, "dados": por_dia}
        garantir_conexao_mqtt()
        try:
            result = mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
            result.wait_for_publish()
            if result.rc != 0:
                logging.error(f"Erro ao publicar no tópico {MQTT_TOPIC}: código {result.rc}")
            else:
                logging.info(f"Publicação bem-sucedida no tópico {MQTT_TOPIC}")
                logging.info(f"Publicado {len(por_dia)} registros por dia para {ultimo_dia_processado}")
        except Exception as e:
            logging.error(f"Exceção ao tentar publicar: {str(e)}")

        buffer_diario = [
            r for r in buffer_diario
            if datetime.fromisoformat(r["timestamp"]).replace(hour=0, minute=0, second=0, microsecond=0) > ultimo_dia_processado
        ]

        ultimo_dia_processado += timedelta(days=1)

# função principal que mantém conexão com o CLP e executa leitura, processamento e envio periódico dos dados
async def main():
    while True:
        client = Client(url=OPC_URL)

        try:
            await client.connect()
            logging.info("Conectado ao CLP")

            while True:
                try:
                    leitura = await ler_clp(client)
                    processar_leitura(leitura)

                    agora = datetime.fromisoformat(leitura["timestamp"])
                    hora_atual = agora.replace(minute=0, second=0, microsecond=0)
                    dia_atual = agora.replace(hour=0, minute=0, second=0, microsecond=0)

                    verificar_e_publicar_hora(hora_atual)
                    verificar_e_publicar_dia(dia_atual)

                    await asyncio.sleep(INTERVALO_SEGUNDOS)

                except Exception as e:
                    logging.error(f"Erro ao ler do CLP: {str(e)}")
                    break

        except Exception as e:
            logging.error(f"Erro ao conectar ao CLP: {str(e)}")

        finally:
            try:
                await client.disconnect()
                logging.info("Desconectado do CLP")
            except:
                pass

        logging.info("Tentando reconectar ao CLP em 5 segundos...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())

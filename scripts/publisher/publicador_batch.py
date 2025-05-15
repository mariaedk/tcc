import asyncio
from asyncua import Client
from datetime import datetime
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

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    logging.info("Conectado ao broker MQTT")
except Exception as e:
    logging.error(f"Erro ao conectar no broker: {str(e)}")
    raise

buffer_leituras = []
ultima_hora_processada = None
ultimo_dia_processado = None


async def ler_clp(client):
    """
    Realiza a leitura dos sensores definidos na configuração via OPC UA.

    Para cada sensor:
    - Tenta ler o valor do node;
    - Caso o valor seja numérico, armazena no dicionário de leitura;
    - Caso contrário, registra falha e armazena 0.0 como valor.

    Retorna:
        dict: Dicionário contendo timestamp, valores lidos e flag de falha.
    """
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
    """
    Agrupa registros por hora ou por dia e calcula a média dos valores para cada sensor.

    Args:
        registros (list): Lista de leituras individuais.
        tipo (str): Define o tipo de agrupamento, podendo ser horário ou diário.

    Retorna:
        list: Lista de dicionários com dados agrupados, contendo data, tipo_sensor,
              média do valor, flag de falha e tipo de dispositivo.
    """
    agrupado = defaultdict(list)

    for r in registros:
        ts = datetime.fromisoformat(r["timestamp"])
        chave = ts.replace(minute=0, second=0, microsecond=0) if tipo == TIPO_AGRUPAMENTO_HORA else ts.replace(hour=0, minute=0, second=0, microsecond=0)

        for tipo_sensor, valor in r["valores"].items():
            agrupado[(chave.isoformat(), tipo_sensor)].append(valor)

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

async def main():
    """
    Função principal que executa o ciclo de:
    - Conectar ao CLP;
    - Ler valores dos sensores;
    - Armazenar os dados em buffer;
    - Agrupar e publicar os dados por hora e por dia conforme o tempo avança;
    - Publicar os dados no broker MQTT.
    """
    global ultima_hora_processada, ultimo_dia_processado
    client = Client(url=OPC_URL)

    try:
        await client.connect()
        logging.info("Conectado ao CLP")

        while True:
            leitura = await ler_clp(client)
            buffer_leituras.append(leitura)
            logging.info(f"Leitura adicionada: {leitura}")

            agora = datetime.fromisoformat(leitura["timestamp"])
            hora_atual = agora.replace(minute=0, second=0, microsecond=0)
            dia_atual = agora.replace(hour=0, minute=0, second=0, microsecond=0)

            # processar o agrupado por hora
            if ultima_hora_processada and hora_atual > ultima_hora_processada:
                registros_hora = [r for r in buffer_leituras if datetime.fromisoformat(r["timestamp"]).replace(minute=0, second=0, microsecond=0) == ultima_hora_processada]
                por_hora = agrupar_e_publicar(registros_hora, tipo=TIPO_AGRUPAMENTO_HORA)
                payload = {"tipo": TIPO_AGRUPAMENTO_HORA, "dados": por_hora}
                mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
                logging.info(f"Publicado {len(por_hora)} registros por hora para {ultima_hora_processada}")

                # limpeza dos registros por hora
                buffer_leituras = [r for r in buffer_leituras if datetime.fromisoformat(r["timestamp"]).replace(minute=0, second=0, microsecond=0) > ultima_hora_processada]

            # agrupamento do dia
            if ultimo_dia_processado and dia_atual > ultimo_dia_processado:
                registros_dia = [r for r in buffer_leituras if datetime.fromisoformat(r["timestamp"]).replace(hour=0, minute=0, second=0, microsecond=0) == ultimo_dia_processado]
                por_dia = agrupar_e_publicar(registros_dia, tipo=TIPO_AGRUPAMENTO_DIA)
                payload = {"tipo": TIPO_AGRUPAMENTO_DIA, "dados": por_dia}
                mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
                logging.info(f"Publicado {len(por_dia)} registros por dia para {ultimo_dia_processado}")

                # limpeza dos registros
                buffer_leituras = [r for r in buffer_leituras if datetime.fromisoformat(r["timestamp"]).replace(hour=0, minute=0, second=0, microsecond=0) > ultimo_dia_processado]

            ultima_hora_processada = hora_atual
            ultimo_dia_processado = dia_atual

            await asyncio.sleep(INTERVALO_SEGUNDOS)

    finally:
        await client.disconnect()
        logging.info("Desconectado do CLP")

if __name__ == "__main__":
    asyncio.run(main())

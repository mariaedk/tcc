"""
@author maria
date: 2025-05-25
"""
import fdb
import requests
from tqdm import tqdm
import logging
from datetime import datetime
from config import (
    FIREBIRD_PATH, FIREBIRD_USER, FIREBIRD_PASSWORD,
    API_URL, AUTH_URL, USERNAME, PASSWORD,
    SENSOR_VAZAO1_ID, SENSOR_VAZAO2_ID,
    UNIDADE_ID, TIPO_MEDICAO, BATCH_SIZE
)

logging.basicConfig(
    filename="importador_fdb.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def obter_token():
    try:
        response = requests.post(AUTH_URL, data={
            "username": USERNAME,
            "password": PASSWORD
        })
        response.raise_for_status()
        data = response.json()
        token = data["access_token"]
        logging.info("Token obtido com sucesso.")
        return token
    except Exception as e:
        if hasattr(e, 'response') and e.response is not None:
            logging.error(f"Resposta da API: {e.response.text}")
            print(e.response.text)  # Debug na tela
        logging.error(f"Erro ao obter token: {e}")
        raise

con = fdb.connect(
    dsn=FIREBIRD_PATH,
    user=FIREBIRD_USER,
    password=FIREBIRD_PASSWORD
)
cur = con.cursor()

sql = """
SELECT HIF_DATAHORA, 
       HIF_ETA1_MV1_VAZAO, 
       HIF_ETA2_MV1_VAZAO
FROM HISTINFO
"""

cur.execute(sql)
registros = cur.fetchall()
total = len(registros)
print(f"Total de registros encontrados: {total}")

token = obter_token()
headers = {"Authorization": f"Bearer {token}"}

lote = []

for row in tqdm(registros, desc="enviando registros"):
    data_hora, vazao_1, vazao_2 = row

    if not isinstance(data_hora, datetime):
        logging.warning(f"Data inválida em registro: {row}")
        continue

    coleta = {
        "origem": "CLP",
        "data_hora": data_hora.isoformat(),
        "medicoes": [
            {
                "sensor_id": SENSOR_VAZAO1_ID,
                "unidade_id": UNIDADE_ID,
                "valor": float(vazao_1) if vazao_1 is not None else 0,
                "valor_str": None,
                "valor_bool": None,
                "data_hora": data_hora.isoformat(),
                "falha": False,
                "tipo": TIPO_MEDICAO
            },
            {
                "sensor_id": SENSOR_VAZAO2_ID,
                "unidade_id": UNIDADE_ID,
                "valor": float(vazao_2) if vazao_2 is not None else 0,
                "valor_str": None,
                "valor_bool": None,
                "data_hora": data_hora.isoformat(),
                "falha": False,
                "tipo": TIPO_MEDICAO
            }
        ]
    }

    lote.append(coleta)

    if len(lote) >= BATCH_SIZE:
        try:
            response = requests.post(API_URL + "/batch", json=lote, headers=headers)
            response.raise_for_status()
            logging.info(f"Lote com {len(lote)} registros enviado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao enviar lote: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Resposta da API: {e.response.text}")
                print(e.response.text)
        lote.clear()

if lote:
    try:
        response = requests.post(API_URL + "/batch", json=lote, headers=headers)
        response.raise_for_status()
        logging.info(f"Último lote com {len(lote)} registros enviado com sucesso")
    except Exception as e:
        logging.error(f"Erro ao enviar o último lote: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logging.error(f"Resposta da API: {e.response.text}")
            print(e.response.text)

cur.close()
con.close()
print("Importação finalizada.")

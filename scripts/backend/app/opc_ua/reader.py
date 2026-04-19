import asyncio
import logging
import os
from datetime import datetime, timezone

from asyncua import Client
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.coleta_model import Coleta
from app.models.enums import TipoMedicao
from app.models.medicao_model import Medicao
from app.models.sensor_model import Sensor
from app.models.unidade_medida_model import UnidadeMedida

logger = logging.getLogger(__name__)

INTERVALO_SEGUNDOS = int(os.getenv("OPC_INTERVALO", 10))
OPC_URL = os.getenv("OPC_URL")
OPC_USERNAME = os.getenv("OPC_USERNAME")
OPC_PW = os.getenv("OPC_PW")

SENSORES = {
    "VAZAO_SAIDA1": os.getenv("OPC_NODE_VAZAO1"),
    "VAZAO_SAIDA2": os.getenv("OPC_NODE_VAZAO2"),
}

SENSOR_NOME_MAP = {
    "VAZAO_SAIDA1": "Vazão Saída 1",
    "VAZAO_SAIDA2": "Vazão Saída 2",
}


def _gravar_leitura(valores: dict, falha: bool):
    db: Session = SessionLocal()
    try:
        unidade = db.query(UnidadeMedida).filter_by(sigla="L/min").first()

        coleta = Coleta(data_hora=datetime.now(timezone.utc), origem="OPC_UA")
        db.add(coleta)
        db.flush()

        for chave, valor in valores.items():
            nome_sensor = SENSOR_NOME_MAP.get(chave)
            sensor = db.query(Sensor).filter_by(nome=nome_sensor).first()
            if sensor and unidade:
                db.add(Medicao(
                    coleta_id=coleta.id,
                    sensor_id=sensor.id,
                    unidade_id=unidade.id,
                    valor=valor,
                    tipo=TipoMedicao.INST,
                    falha=falha,
                    data_hora=datetime.now(timezone.utc),
                ))

        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao gravar leitura: {e}")
    finally:
        db.close()


async def loop_opc_ua():
    if not OPC_URL:
        logger.warning("OPC_URL não configurada — leitura OPC UA desativada.")
        return

    while True:
        client = Client(url=OPC_URL)
        if OPC_USERNAME:
            client.set_user(OPC_USERNAME)
            client.set_password(OPC_PW or "")

        try:
            await client.connect()
            logger.info("Conectado ao CLP via OPC UA")

            while True:
                valores = {}
                falha = False

                for nome, node_id in SENSORES.items():
                    if not node_id:
                        continue
                    try:
                        valor = await client.get_node(node_id).read_value()
                        valores[nome] = float(valor) if isinstance(valor, (float, int)) else 0.0
                        if not isinstance(valor, (float, int)):
                            falha = True
                    except Exception as e:
                        logger.error(f"Erro ao ler {nome}: {e}")
                        valores[nome] = 0.0
                        falha = True

                if valores:
                    _gravar_leitura(valores, falha)

                await asyncio.sleep(INTERVALO_SEGUNDOS)

        except asyncio.CancelledError:
            raise
        except Exception as e:
            logger.error(f"Conexão OPC UA falhou: {e}")
        finally:
            try:
                await client.disconnect()
            except Exception:
                pass

        logger.info("Reconectando ao CLP em 10 segundos...")
        await asyncio.sleep(10)

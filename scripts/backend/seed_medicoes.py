"""
Insere 30 dias de medições simuladas (intervalo de 10s) para os dois sensores.
Executar: docker compose exec backend python seed_medicoes.py
"""
import random
import math
from datetime import datetime, timedelta, timezone
from sqlalchemy import insert
from app.database import SessionLocal
from app.models.coleta_model import Coleta
from app.models.medicao_model import Medicao
from app.models.sensor_model import Sensor
from app.models.unidade_medida_model import UnidadeMedida

DIAS = 30
INTERVALO_SEGUNDOS = 10
BATCH_SIZE = 500


def valor_simulado(sensor_nome: str, ts: datetime) -> float:
    hora = ts.hour + ts.minute / 60
    curva = 1.0 + 0.3 * math.sin((hora - 6) * math.pi / 12)
    base = 950 if sensor_nome == "Vazão Saída 1" else 750
    return round(max(0, base * curva + random.gauss(0, 15)), 2)


def seed():
    db = SessionLocal()
    try:
        unidade = db.query(UnidadeMedida).filter_by(sigla="L/min").first()
        sensor1 = db.query(Sensor).filter_by(nome="Vazão Saída 1").first()
        sensor2 = db.query(Sensor).filter_by(nome="Vazão Saída 2").first()

        if not unidade or not sensor1 or not sensor2:
            print("Erro: unidade ou sensores não encontrados.")
            return

        agora = datetime.now(timezone.utc)
        inicio = agora - timedelta(days=DIAS)
        total = int(DIAS * 24 * 3600 / INTERVALO_SEGUNDOS)
        print(f"Inserindo {total} coletas ({total * 2} medições)...")

        timestamps = [
            inicio + timedelta(seconds=i * INTERVALO_SEGUNDOS)
            for i in range(total + 1)
            if inicio + timedelta(seconds=i * INTERVALO_SEGUNDOS) <= agora
        ]

        inseridos = 0
        for i in range(0, len(timestamps), BATCH_SIZE):
            lote_ts = timestamps[i:i + BATCH_SIZE]

            coleta_rows = [{"dt_hora": ts, "origem": "SIMULADO"} for ts in lote_ts]
            result = db.execute(insert(Coleta).returning(Coleta.id), coleta_rows)
            ids = [row[0] for row in result]

            medicao_rows = []
            for coleta_id, ts in zip(ids, lote_ts):
                for sensor in [sensor1, sensor2]:
                    medicao_rows.append({
                        "coleta_id": coleta_id,
                        "sensor_id": sensor.id,
                        "unidade_id": unidade.id,
                        "valor": valor_simulado(sensor.nome, ts),
                        "tipo": "INST",
                        "falha": False,
                        "data_hora": ts,
                    })

            db.execute(insert(Medicao), medicao_rows)
            db.commit()
            inseridos += len(lote_ts)
            print(f"  {inseridos}/{len(timestamps)} coletas inseridas...")

        print(f"Concluído! {inseridos} coletas e {inseridos * 2} medições inseridas.")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()

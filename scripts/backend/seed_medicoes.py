from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.dispositivo_model import Dispositivo
from app.models.sensor_model import Sensor
from app.models.unidade_medida_model import UnidadeMedida
from app.models.coleta_model import Coleta
from app.models.medicao_model import Medicao
from app.models.enums import TipoDispositivo, TipoSensor
import random

UTC = timezone.utc

def criar_dispositivos_e_sensores(db: Session):
    dispositivos = [
        {"nome": "CLP", "tipo": TipoDispositivo.CLP, "localizacao": "ETA", "codigo": 1}
    ]
    sensores = [
        {"nome": "vazao_entrada", "tipo": TipoSensor.VAZAO, "codigo": 1},
        {"nome": "vazao_saida", "tipo": TipoSensor.VAZAO, "codigo": 2},
        {"nome": "nivel", "tipo": TipoSensor.NIVEL, "codigo": 3},
    ]
    unidades = [
        {"denominacao": "Litros por segundo", "sigla": "L/s"},
        {"denominacao": "Litros", "sigla": "L"},
    ]

    if db.query(Dispositivo).count() == 0:
        for d in dispositivos:
            db.add(Dispositivo(**d))
        db.commit()

    dispositivo = db.query(Dispositivo).filter_by(codigo=1).first()

    if db.query(Sensor).count() == 0:
        for s in sensores:
            db.add(Sensor(**s, dispositivo_id=dispositivo.id))
        db.commit()

    if db.query(UnidadeMedida).count() == 0:
        for u in unidades:
            db.add(UnidadeMedida(**u))
        db.commit()

def popular_medicoes_instantaneas(db: Session):
    sensores = {s.codigo: s for s in db.query(Sensor).all()}
    unidades = {u.sigla: u for u in db.query(UnidadeMedida).all()}
    agora = datetime.now(UTC)
    inicio = agora - timedelta(days=5)
    inicio = inicio.replace(second=0, microsecond=0)

    total = 0
    data_hora = inicio

    while data_hora <= agora:
        coleta = Coleta(data_hora=data_hora, origem="simulado")
        db.add(coleta)
        db.flush()

        medicoes = [
            Medicao(
                coleta_id=coleta.id,
                sensor_id=sensores[1].id,
                unidade_id=unidades["L/s"].id,
                valor=round(random.uniform(19, 23), 2),
                data_hora=data_hora,
                tipo="INST",
                falha=False
            ),
            Medicao(
                coleta_id=coleta.id,
                sensor_id=sensores[2].id,
                unidade_id=unidades["L/s"].id,
                valor=round(random.uniform(17, 21), 2),
                data_hora=data_hora,
                tipo="INST",
                falha=False
            ),
            Medicao(
                coleta_id=coleta.id,
                sensor_id=sensores[3].id,
                unidade_id=unidades["L"].id,
                valor=round(random.uniform(2500, 5000), 2),
                data_hora=data_hora,
                tipo="INST",
                falha=False
            )
        ]

        db.add_all(medicoes)
        total += len(medicoes)

        data_hora += timedelta(minutes=3)

    db.commit()
    print(f"✅ {total} medições instantâneas inseridas com sucesso.")

def seed():
    db: Session = SessionLocal()
    try:
        criar_dispositivos_e_sensores(db)
        popular_medicoes_instantaneas(db)
    except Exception as e:
        db.rollback()
        print("❌ Erro:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed()

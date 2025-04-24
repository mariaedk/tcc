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
        {"nome": "nivel", "tipo": TipoSensor.PRESSAO, "codigo": 3},
        {"nome": "bomba_ativa", "tipo": TipoSensor.PRESSAO, "codigo": 4},
        {"nome": "status", "tipo": TipoSensor.PRESSAO, "codigo": 5},
        {"nome": "hora", "tipo": TipoSensor.TEMPERATURA, "codigo": 6},
    ]
    unidades = [
        {"denominacao": "Litros por segundo", "sigla": "L/s"},
        {"denominacao": "Status", "sigla": "status"},
        {"denominacao": "Litros", "sigla": "L"},
        {"denominacao": "Texto", "sigla": "texto"}
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

def popular_medicoes(db: Session):
    sensores = {s.codigo: s for s in db.query(Sensor).all()}
    unidades = {u.sigla: u for u in db.query(UnidadeMedida).all()}
    agora = datetime.now(UTC)
    inicio = agora - timedelta(days=30)

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
                valor=round(random.uniform(19, 22), 2),
                data_hora=data_hora
            ),
            Medicao(
                coleta_id=coleta.id,
                sensor_id=sensores[2].id,
                unidade_id=unidades["L/s"].id,
                valor=round(random.uniform(17, 20), 2),
                data_hora=data_hora
            ),
            Medicao(
                coleta_id=coleta.id,
                sensor_id=sensores[3].id,
                unidade_id=unidades["L"].id,
                valor=round(random.uniform(2000, 5000), 2),
                data_hora=data_hora
            ),
            Medicao(
                coleta_id=coleta.id,
                sensor_id=sensores[4].id,
                unidade_id=unidades["status"].id,
                valor_bool=random.choice([True, False]),
                data_hora=data_hora
            ),
            Medicao(
                coleta_id=coleta.id,
                sensor_id=sensores[5].id,
                unidade_id=unidades["texto"].id,
                valor_str="12:00",
                data_hora=data_hora
            )
        ]

        db.add_all(medicoes)
        total += len(medicoes)
        data_hora += timedelta(seconds=10)

    db.commit()
    print(f"✅ {total} medições inseridas com sucesso.")

def seed():
    db: Session = SessionLocal()
    try:
        criar_dispositivos_e_sensores(db)
        popular_medicoes(db)
    except Exception as e:
        db.rollback()
        print("❌ Erro:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed()

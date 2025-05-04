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

def popular_medicoes(db: Session):
    sensores = {s.codigo: s for s in db.query(Sensor).all()}
    unidades = {u.sigla: u for u in db.query(UnidadeMedida).all()}
    agora = datetime.now(UTC)
    inicio = agora - timedelta(days=30)
    inicio = inicio.replace(hour=0, minute=0, second=0, microsecond=0)

    total = 0
    data_hora = inicio

    while data_hora <= agora:
        # MÉDIA POR HORA
        coleta_hora = Coleta(data_hora=data_hora, origem="simulado")
        db.add(coleta_hora)
        db.flush()

        valores_hora = {
            "vazao_entrada": round(random.uniform(19, 22), 2),
            "vazao_saida": round(random.uniform(17, 20), 2),
            "nivel": round(random.uniform(2000, 5000), 2)
        }

        medicoes_hora = [
            Medicao(
                coleta_id=coleta_hora.id,
                sensor_id=sensores[1].id,
                unidade_id=unidades["L/s"].id,
                valor=valores_hora["vazao_entrada"],
                data_hora=data_hora,
                tipo="HORA",
                falha=False
            ),
            Medicao(
                coleta_id=coleta_hora.id,
                sensor_id=sensores[2].id,
                unidade_id=unidades["L/s"].id,
                valor=valores_hora["vazao_saida"],
                data_hora=data_hora,
                tipo="HORA",
                falha=False
            ),
            Medicao(
                coleta_id=coleta_hora.id,
                sensor_id=sensores[3].id,
                unidade_id=unidades["L"].id,
                valor=valores_hora["nivel"],
                data_hora=data_hora,
                tipo="HORA",
                falha=False
            )
        ]

        db.add_all(medicoes_hora)
        total += len(medicoes_hora)

        # SE HORA == 00:00, GERAR MÉDIA POR DIA
        if data_hora.hour == 0:
            coleta_dia = Coleta(data_hora=data_hora, origem="simulado")
            db.add(coleta_dia)
            db.flush()

            valores_dia = {
                "vazao_entrada": round(random.uniform(19, 22), 2),
                "vazao_saida": round(random.uniform(17, 20), 2),
                "nivel": round(random.uniform(2000, 5000), 2)
            }

            medicoes_dia = [
                Medicao(
                    coleta_id=coleta_dia.id,
                    sensor_id=sensores[1].id,
                    unidade_id=unidades["L/s"].id,
                    valor=valores_dia["vazao_entrada"],
                    data_hora=data_hora,
                    tipo="DIA",
                    falha=False
                ),
                Medicao(
                    coleta_id=coleta_dia.id,
                    sensor_id=sensores[2].id,
                    unidade_id=unidades["L/s"].id,
                    valor=valores_dia["vazao_saida"],
                    data_hora=data_hora,
                    tipo="DIA",
                    falha=False
                ),
                Medicao(
                    coleta_id=coleta_dia.id,
                    sensor_id=sensores[3].id,
                    unidade_id=unidades["L"].id,
                    valor=valores_dia["nivel"],
                    data_hora=data_hora,
                    tipo="DIA",
                    falha=False
                )
            ]

            db.add_all(medicoes_dia)
            total += len(medicoes_dia)

        data_hora += timedelta(hours=1)

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

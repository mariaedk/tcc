from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.dispositivo_model import Dispositivo
from app.models.sensor_model import Sensor
from app.models.unidade_medida_model import UnidadeMedida
from app.models.medicao_model import Medicao
from app.models.enums import TipoDispositivo, TipoSensor
import random

UTC = timezone.utc

# Configurações
TOTAL_POR_SENSOR = 100
INTERVALO_MINUTOS = 10

def criar_dispositivos_e_sensores(db: Session):
    dispositivos = [
        {"nome": "Dispositivo A", "tipo": TipoDispositivo.RASPBERRY, "localizacao": "Setor 1"},
        {"nome": "Dispositivo B", "tipo": TipoDispositivo.CLP, "localizacao": "Setor 2"},
    ]
    sensores = [
        {"nome": "Sensor de Vazão", "tipo": TipoSensor.VAZAO, "dispositivo_idx": 0},
        {"nome": "Sensor de Pressão", "tipo": TipoSensor.PRESSAO, "dispositivo_idx": 0},
        {"nome": "Sensor de Temperatura", "tipo": TipoSensor.TEMPERATURA, "dispositivo_idx": 1},
    ]
    unidades = [
        {"denominacao": "Litros por Minuto", "sigla": "L/min"},
        {"denominacao": "Bar", "sigla": "bar"},
        {"denominacao": "Metros", "sigla": "m"},
        {"denominacao": "Graus Celsius", "sigla": "°C"},
    ]

    # Inserir dispositivos se estiverem vazios
    if db.query(Dispositivo).count() == 0:
        db.add_all([Dispositivo(**d) for d in dispositivos])
        db.commit()
        print("✓ Dispositivos inseridos.")

    # Obter dispositivos com ID já preenchido
    dispositivos_db = db.query(Dispositivo).all()

    # Inserir sensores se estiverem vazios
    if db.query(Sensor).count() == 0:
        sensores_objs = []
        for s in sensores:
            dispositivo = dispositivos_db[s["dispositivo_idx"]]
            sensores_objs.append(Sensor(
                nome=s["nome"],
                tipo=s["tipo"],
                dispositivo_id=dispositivo.id
            ))
        db.add_all(sensores_objs)
        db.commit()
        print("✓ Sensores inseridos.")

    # Inserir unidades de medida se estiverem vazias
    if db.query(UnidadeMedida).count() == 0:
        db.add_all([UnidadeMedida(**u) for u in unidades])
        db.commit()
        print("✓ Unidades de medida inseridas.")

def gerar_medicoes(sensor_id, unidade_id, minimo, maximo):
    agora = datetime.now(UTC)
    inicio = agora - timedelta(days=30)
    medicoes = []

    intervalo = timedelta(minutes=10)
    atual = inicio

    while atual <= agora:
        valor = round(random.uniform(minimo, maximo), 2)
        medicoes.append(Medicao(
            sensor_id=sensor_id,
            unidade_id=unidade_id,
            valor=valor,
            data_hora=atual
        ))
        atual += intervalo

    return medicoes

def popular_medicoes(db: Session):
    sensores = db.query(Sensor).all()
    unidades = db.query(UnidadeMedida).all()

    sensores_info = {
        "Sensor de Vazão": {"unidade_sigla": "L/min", "min": 19.0, "max": 22.0},
        "Sensor de Pressão": {"unidade_sigla": "bar", "min": 1.0, "max": 1.5},
        "Sensor de Nível": {"unidade_sigla": "m", "min": 3.5, "max": 4.5},
        "Sensor de Temperatura": {"unidade_sigla": "°C", "min": 24.0, "max": 27.0}
    }

    total = 0
    for sensor in sensores:
        config = sensores_info.get(sensor.nome)
        if config:
            unidade = next((u for u in unidades if u.sigla == config["unidade_sigla"]), None)
            if unidade:
                medicoes = gerar_medicoes(sensor.id, unidade.id, config["min"], config["max"])
                db.add_all(medicoes)
                print(f"✓ Inserido {len(medicoes)} medições para {sensor.nome}")
                total += len(medicoes)

    db.commit()
    print(f"✅ Total de {total} medições inseridas com sucesso.")

def seed():
    db: Session = SessionLocal()
    try:
        criar_dispositivos_e_sensores(db)
        popular_medicoes(db)
    except Exception as e:
        db.rollback()
        print("❌ Erro durante o seed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    seed()

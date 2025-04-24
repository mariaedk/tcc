"""
@author maria
date: 2025-02-25
"""
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from app.models.medicao_model import Medicao
from sqlalchemy import func
from datetime import datetime, timezone, timedelta
from app.models.sensor_model import Sensor
from app.models.dispositivo_model import Dispositivo

class MedicaoRepository:

    @staticmethod
    def find_all(db: Session) -> list[Medicao]:
        return db.query(Medicao).all()

    @staticmethod
    def find_all_paginate(db: Session, limit: int = 10, offset: int = 0):
        return db.query(Medicao).offset(offset).limit(limit).all()

    @staticmethod
    def save(db: Session, medicao: Medicao) -> Medicao:
        if medicao.id:
            db.merge(medicao)
        else:
            db.add(medicao)
        db.commit()
        db.refresh(medicao)
        return medicao

    @staticmethod
    def find_by_id(db: Session, id: int) -> Medicao | None:
        return db.query(Medicao).filter(Medicao.id == id).first()

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        medicao = db.query(Medicao).filter(Medicao.id == id).first()
        if medicao:
            db.delete(medicao)
            db.commit()

    @staticmethod
    def media_por_dia_por_sensor(db: Session, cd_sensor: int, dias: int = 30):
        data_limite = datetime.now(timezone.utc) - timedelta(days=dias)
        sensor = db.query(Sensor).filter(Sensor.codigo == cd_sensor).first()

        return (
            # busca a data de medição e faz uma média (avg) para cada dia
            db.query(
                func.date(Medicao.data_hora).label("data"),
                func.avg(Medicao.valor).label("media_valor")
            )
            .join(Medicao.sensor)
            .filter(Medicao.sensor_id == sensor.id)
            .filter(Medicao.data_hora >= data_limite)
            .group_by(func.date(Medicao.data_hora))
            .order_by(func.date(Medicao.data_hora))
            .all()
        )

    @staticmethod
    def media_por_dia_por_dispositivo(db: Session, cd_dispositivo: int, dias: int = 30):
        data_limite = datetime.now(timezone.utc) - timedelta(days=dias)

        dispositivo = db.query(Dispositivo).filter(Dispositivo.codigo == cd_dispositivo).first()
        if not dispositivo:
            return []

        sensores_ids = (
            db.query(Sensor.id)
            .filter(Sensor.dispositivo_id == dispositivo.id)
            .all()
        )

        sensor_ids = [s.id for s in sensores_ids]

        resultados = (
            db.query(
                func.date(Medicao.data_hora).label("data"),
                func.avg(Medicao.valor).label("media_valor")
            )
            .filter(Medicao.sensor_id.in_(sensor_ids))
            .filter(Medicao.data_hora >= data_limite)
            .group_by(func.date(Medicao.data_hora))
            .order_by(func.date(Medicao.data_hora))
            .all()
        )

        return resultados

    @staticmethod
    def buscar_por_sensor(db: Session, sensor_id: int):
        return db.query(Medicao).filter(Medicao.sensor_id == sensor_id).all()

    @staticmethod
    def buscar_por_coleta(db: Session, coleta_id: int):
        return db.query(Medicao).filter(Medicao.coleta_id == coleta_id).all()

    @staticmethod
    def buscar_por_unidade(db: Session, unidade_id: int):
        return db.query(Medicao).filter(Medicao.unidade_id == unidade_id).all()

    @staticmethod
    def buscar_por_data_inicio(db: Session, data_inicio: datetime):
        return db.query(Medicao).filter(Medicao.data_hora >= data_inicio).all()

    @staticmethod
    def buscar_por_data_fim(db: Session, data_fim: datetime):
        return db.query(Medicao).filter(Medicao.data_hora <= data_fim).all()

    @staticmethod
    def buscar_por_intervalo_datas(db: Session, data_inicio: datetime, data_fim: datetime):
        return db.query(Medicao).filter(
            Medicao.data_hora >= data_inicio,
            Medicao.data_hora <= data_fim
        ).all()

    @staticmethod
    def comparar_vazoes_por_mes(db: Session, codigo_entrada: int, codigo_saida: int, meses: int = 6):
        # Primeiro dia do mês atual - N meses
        hoje = datetime.now(timezone.utc)
        data_limite = (hoje - relativedelta(months=meses)).replace(day=1)

        resultados = (
            db.query(
                func.date_format(Medicao.data_hora, "%Y-%m").label("mes"),
                Sensor.codigo.label("codigo_sensor"),
                func.avg(Medicao.valor).label("media_valor")
            )
            .join(Medicao.sensor)
            .filter(Sensor.codigo.in_([codigo_entrada, codigo_saida]))
            .filter(Medicao.data_hora >= data_limite)
            .group_by(func.date_format(Medicao.data_hora, "%Y-%m"), Sensor.codigo)
            .order_by(func.date_format(Medicao.data_hora, "%Y-%m"))
            .all()
        )
        return resultados

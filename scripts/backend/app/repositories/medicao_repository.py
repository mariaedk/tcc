"""
@author maria
date: 2025-02-25
"""

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

        return (
            db.query(
                func.date(Medicao.data_hora).label("data"),
                func.avg(Medicao.valor).label("media_valor")
            )
            .filter(Medicao.cd_sensor == cd_sensor)
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


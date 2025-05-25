"""
@author maria
date: 2025-02-25
"""
from collections import defaultdict

from sqlalchemy.orm import Session, joinedload
from app.models.medicao_model import Medicao
from datetime import datetime, timezone, timedelta
from app.models.sensor_model import Sensor
from sqlalchemy.dialects import mysql
from sqlalchemy import extract

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
    def buscar_medicoes_agrupadas(
            db: Session,
            sensor_id: int,
            data: datetime = None,
            data_inicio: datetime = None,
            data_fim: datetime = None,
            dias: int = None,
            tipo: str = None
    ):

        query = db.query(Medicao).options(
            joinedload(Medicao.unidade)
        ).filter(
            Medicao.sensor_id == sensor_id
        )

        if tipo:
            query = query.filter(
                Medicao.tipo == tipo.upper())

        if data:
            inicio = datetime.combine(data.date(), datetime.min.time())
            fim = datetime.combine(data.date(), datetime.max.time())
            query = query.filter(Medicao.data_hora >= inicio, Medicao.data_hora <= fim)

        elif data_inicio and data_fim:
            query = query.filter(Medicao.data_hora >= data_inicio, Medicao.data_hora <= data_fim)

        elif dias:
            limite = datetime.now() - timedelta(days=dias)
            query = query.filter(Medicao.data_hora >= limite)

        # apenas para debugar qual query construiu
        compiled = query.statement.compile(
            dialect=mysql.dialect(),
            compile_kwargs={"literal_binds": True}
        )
        return query.order_by(Medicao.data_hora.asc()).all()

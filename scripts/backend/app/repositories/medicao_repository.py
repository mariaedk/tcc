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
from sqlalchemy import extract, text

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

        return query.order_by(Medicao.data_hora.asc()).all()

    @staticmethod
    def buscar_inst_com_timebucket(
            db: Session,
            sensor_id: int,
            data_inicio: datetime,
            data_fim: datetime,
            intervalo: str
    ):
        sql = text("""
            SELECT
                time_bucket(:intervalo, m.dt_hora) AS data,
                AVG(m.vl_valor) AS valor,
                u.ds_sigla AS unidade
            FROM medicao m
            LEFT JOIN unidade_medida u ON u.id_unidade_medida = m.unidade_medida_id_unidade_medida
            WHERE m.sensor_id_sensor = :sensor_id
              AND m.tp_tipo = 'INST'
              AND m.dt_hora >= :data_inicio
              AND m.dt_hora <= :data_fim
            GROUP BY data, u.ds_sigla
            ORDER BY data ASC
        """)
        result = db.execute(sql, {
            'intervalo': intervalo,
            'sensor_id': sensor_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim
        })
        return result.mappings().all()

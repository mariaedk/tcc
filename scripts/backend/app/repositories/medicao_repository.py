"""
@author maria
date: 2025-02-25
"""
from typing import Optional

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
    def buscar_por_data(db: Session, data: datetime):
        return db.query(Medicao).filter(Medicao.data_hora == data).all()

    @staticmethod
    def buscar_por_intervalo_datas(db: Session, data_inicio: datetime, data_fim: datetime):
        return db.query(Medicao).filter(
            Medicao.data_hora >= data_inicio,
            Medicao.data_hora <= data_fim
        ).all()

    @staticmethod
    def comparar_vazoes_por_mes(
            db: Session,
            codigo_entrada: int,
            codigo_saida: int,
            meses: Optional[int] = 6,
            data_inicio: Optional[datetime] = None,
            data_fim: Optional[datetime] = None
    ):
        hoje = datetime.now(timezone.utc)

        if data_inicio and data_fim:
            filtro_data = (Medicao.data_hora >= data_inicio) & (Medicao.data_hora <= data_fim)
        elif meses:
            data_limite = (hoje - relativedelta(months=meses)).replace(day=1)
            filtro_data = Medicao.data_hora >= data_limite
        else:
            filtro_data = True

        resultados = (
            db.query(
                func.date_format(Medicao.data_hora, "%Y-%m").label("mes"),
                Sensor.codigo.label("codigo_sensor"),
                func.avg(Medicao.valor).label("media_valor")
            )
            .join(Medicao.sensor)
            .filter(Sensor.codigo.in_([codigo_entrada, codigo_saida]))
            .filter(filtro_data)
            .group_by(func.date_format(Medicao.data_hora, "%Y-%m"), Sensor.codigo)
            .order_by(func.date_format(Medicao.data_hora, "%Y-%m"))
            .all()
        )
        return resultados

    @staticmethod
    def buscar_medicoes_geral(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                              data_fim: datetime = None, dias: int = None):
        sensor = db.query(Sensor).filter(Sensor.codigo == sensor_codigo).first()
        if not sensor:
            return []

        query = (
            db.query(
                func.date_format(Medicao.data_hora, "%Y-%m-%d %H:00:00").label("data_hora"),
                func.avg(Medicao.valor).label("media_valor")
            )
            .join(Medicao.sensor)
            .filter(Medicao.sensor_id == sensor.id)
        )

        if data:
            query = query.filter(func.date(Medicao.data_hora) == data.date())
        elif data_inicio and data_fim:
            query = query.filter(Medicao.data_hora >= data_inicio, Medicao.data_hora <= data_fim)
        elif dias:
            data_limite = datetime.now(timezone.utc) - timedelta(days=dias)
            query = query.filter(Medicao.data_hora >= data_limite)

        return query.group_by(func.date_format(Medicao.data_hora, "%Y-%m-%d %H")).order_by(
            func.date_format(Medicao.data_hora, "%Y-%m-%d %H")).all()

    @staticmethod
    def buscar_medicoes_por_hora(db: Session, sensor_codigo: int, data: datetime):
        sensor = db.query(Sensor).filter(Sensor.codigo == sensor_codigo).first()
        if not sensor:
            return []

        inicio = datetime.combine(data.date(), datetime.min.time())
        fim = datetime.combine(data.date(), datetime.max.time())

        query = (
            db.query(
                func.date_format(Medicao.data_hora, "%Y-%m-%d %H:00:00").label("data_hora"),
                func.avg(Medicao.valor).label("media_valor")
            )
            .join(Medicao.sensor)
            .filter(Medicao.sensor_id == sensor.id)
            .filter(Medicao.data_hora >= inicio, Medicao.data_hora <= fim)
            .group_by(func.date_format(Medicao.data_hora, "%Y-%m-%d %H"))
            .order_by(func.date_format(Medicao.data_hora, "%Y-%m-%d %H"))
        )

        return query.all()

    @staticmethod
    def buscar_medicoes_media_por_dia(db: Session, sensor_codigo: int, data: datetime = None,
                                      data_inicio: datetime = None, data_fim: datetime = None, dias: int = None):
        query = db.query(
            func.date(Medicao.data_hora).label("data"),
            func.avg(Medicao.valor).label("media_valor")
        ).join(Medicao.sensor).filter(Sensor.codigo == sensor_codigo)

        if data:
            query = query.filter(func.date(Medicao.data_hora) == data.date())
        elif data_inicio and data_fim:
            query = query.filter(Medicao.data_hora >= data_inicio, Medicao.data_hora <= data_fim)
        elif dias:
            data_limite = datetime.now(timezone.utc) - timedelta(days=dias)
            query = query.filter(Medicao.data_hora >= data_limite)

        return query.group_by(func.date(Medicao.data_hora)).order_by(func.date(Medicao.data_hora)).all()

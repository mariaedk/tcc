"""
@author maria
date: 2025-02-27
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Sensor
from app.schemas.medicao_schema import MedicaoCreate, MedicaoResponse, MedicaoHistoricoSchema
from app.repositories.medicao_repository import MedicaoRepository
from app.config import MessageLoader
from sqlalchemy.exc import InvalidRequestError, DatabaseError
from app.models.medicao_model import Medicao
from datetime import datetime, time

class MedicaoService:

    @staticmethod
    def criar_medicao(db: Session, medicao_schema: MedicaoCreate) -> MedicaoResponse:
        if medicao_schema is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        medicao_dict = medicao_schema.model_dump()
        medicao_obj = Medicao(**medicao_dict)

        try:
            medicao = MedicaoRepository.save(db, medicao_obj)
        except InvalidRequestError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.requisicao_invalida"))
        except DatabaseError:
            db.rollback()
            raise HTTPException(status_code=500, detail=MessageLoader.get("erro.banco"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        return MedicaoResponse.model_validate(medicao)

    @staticmethod
    def listar_medicoes(db: Session):
        medicoes = MedicaoRepository.find_all(db)
        return [MedicaoResponse.model_validate(medicao) for medicao in medicoes]

    @staticmethod
    def listar_medicoes_paginadas(db: Session, limit: int = 10, offset: int = 0):
        medicoes = MedicaoRepository.find_all_paginate(db, limit, offset)
        return [MedicaoResponse.model_validate(medicao) for medicao in medicoes]

    @staticmethod
    def buscar_medicao(db: Session, medicao_id: int):
        if medicao_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        medicao = MedicaoRepository.find_by_id(db, medicao_id)
        if not medicao:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.medicao_nao_encontrada"))

        return MedicaoResponse.model_validate(medicao)

    @staticmethod
    def _calcular_intervalo_bucket(data_inicio: datetime, data_fim: datetime) -> str | None:
        horas = (data_fim - data_inicio).total_seconds() / 3600
        if horas <= 24:
            return None
        elif horas <= 72:
            return '1 minute'
        elif horas <= 168:
            return '5 minutes'
        else:
            return '15 minutes'

    @staticmethod
    def buscar_medicoes(
        db: Session,
        sensor_codigo: int,
        tipo: str,
        data: datetime = None,
        data_inicio: datetime = None,
        data_fim: datetime = None,
        dias: int = None
    ) -> list[MedicaoHistoricoSchema]:

        if data_fim and data_fim.time() == time(0, 0, 0):
            data_fim = data_fim.replace(hour=23, minute=59, second=59, microsecond=999999)

        sensor = db.query(Sensor).filter(Sensor.codigo == sensor_codigo).first()
        if not sensor:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        if tipo.upper() == 'INST' and data_inicio and data_fim:
            intervalo = MedicaoService._calcular_intervalo_bucket(data_inicio, data_fim)
            if intervalo:
                resultados = MedicaoRepository.buscar_inst_com_timebucket(
                    db=db,
                    sensor_id=sensor.id,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    intervalo=intervalo
                )
                return [
                    MedicaoHistoricoSchema(
                        data=row['data'],
                        valor=round(row['valor'], 2),
                        unidade=row['unidade']
                    ) for row in resultados
                ]

        resultados = MedicaoRepository.buscar_medicoes_agrupadas(
            db=db,
            sensor_id=sensor.id,
            data=data,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dias=dias,
            tipo=tipo
        )

        return [
            MedicaoHistoricoSchema(
                data=m.data_hora,
                valor=round(m.valor, 2),
                unidade=m.unidade.sigla if m.unidade else None
            ) for m in resultados
        ]

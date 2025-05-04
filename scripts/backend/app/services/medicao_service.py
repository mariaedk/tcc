"""
@author maria
date: 2025-02-27
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.medicao_schema import MedicaoCreate, MedicaoResponse, MedicaoHistoricoSchema
from app.repositories.medicao_repository import MedicaoRepository
from app.config import MessageLoader
from sqlalchemy.exc import InvalidRequestError, DatabaseError
from app.models.medicao_model import Medicao
from datetime import datetime

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
    def buscar_medicoes_por_hora(db: Session, sensor_codigo: int, data: datetime = None) -> list[MedicaoHistoricoSchema]:
        medicoes = MedicaoRepository.buscar_medicoes_agrupadas(db, sensor_codigo, data, tipo='hora')
        return [
            MedicaoHistoricoSchema(data=m.data_hora, valor=round(m.valor, 2))
            for m in medicoes
        ]

    @staticmethod
    def buscar_medicoes_media_por_dia(db: Session, sensor_codigo: int, data: datetime = None,
                                      data_inicio: datetime = None, data_fim: datetime = None,
                                      dias: int = None) -> list[MedicaoHistoricoSchema]:
        if not sensor_codigo:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        medicoes = MedicaoRepository.buscar_medicoes_agrupadas(db, sensor_codigo, data, data_inicio, data_fim, dias, tipo='dia')
        return [
            MedicaoHistoricoSchema(data=m.data_hora, valor=round(m.valor, 2))
            for m in medicoes
        ]

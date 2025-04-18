"""
@author maria
date: 2025-04-17
"""
from fastapi import HTTPException
from sqlalchemy.exc import InvalidRequestError, DatabaseError
from sqlalchemy.orm import Session
from app.schemas.coleta_schema import ColetaCreate, ColetaResponse
from app.models.coleta_model import Coleta
from app.models.medicao_model import Medicao
from app.repositories.coleta_repository import ColetaRepository
from app.config import MessageLoader

class ColetaService:

    @staticmethod
    def criar_coleta(db: Session, coleta_schema: ColetaCreate) -> ColetaResponse:
        if not coleta_schema or not coleta_schema.medicoes:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        coleta_dict = coleta_schema.model_dump()
        medicoes_data = coleta_dict.pop("medicoes")

        coleta_obj = Coleta(**coleta_dict)
        coleta_obj.medicoes = [Medicao(**m) for m in medicoes_data]

        try:
            coleta = ColetaRepository.save(db, coleta_obj)
        except InvalidRequestError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.requisicao_invalida"))
        except DatabaseError:
            db.rollback()
            raise HTTPException(status_code=500, detail=MessageLoader.get("erro.banco"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        return ColetaResponse.model_validate(coleta)

    @staticmethod
    def listar_coletas(db: Session):
        coletas = ColetaRepository.find_all(db)
        return [ColetaResponse.model_validate(c) for c in coletas]

    @staticmethod
    def listar_coletas_paginadas(db: Session, limit: int = 10, offset: int = 0):
        coletas = ColetaRepository.find_all_paginate(db, limit, offset)
        return [ColetaResponse.model_validate(c) for c in coletas]

    @staticmethod
    def buscar_coleta(db: Session, coleta_id: int):
        if coleta_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        coleta = ColetaRepository.find_by_id(db, coleta_id)
        if not coleta:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.nao_encontrado"))

        return ColetaResponse.model_validate(coleta)

"""
@author maria
date: 2025-02-25
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DataError, InvalidRequestError, StatementError, DatabaseError
from app.schemas.dispositivo_schema import DispositivoCreate, DispositivoResponse, DispositivoUpdate
from app.config import MessageLoader
from fastapi import HTTPException
import app.repositories.dispositivo_repository as dispositivo_repository

class DispositivoService:

    @staticmethod
    def criar_dispositivo(db: Session, dispositivo_schema: DispositivoCreate) -> DispositivoResponse:
        if dispositivo_schema is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        dispositivo_dict = dispositivo_schema.model_dump()

        try:
            dispositivo = dispositivo_repository.save(db, dispositivo_dict)
        except DataError: # campo grande
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.tamanho_dados"))
        except InvalidRequestError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.requisicao_invalida"))
        except StatementError: # valor do enum inválido
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.valor_invalido"))
        except DatabaseError:
            db.rollback()
            raise HTTPException(status_code=500, detail=MessageLoader.get("erro.banco"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        dispositivo_response = DispositivoResponse.model_validate(dispositivo)
        return dispositivo_response

    @staticmethod
    def listar_dispositivos(db: Session):
        dispositivos = dispositivo_repository.find_all(db)
        return [DispositivoResponse.model_validate(dispositivo) for dispositivo in dispositivos]

    @staticmethod
    def listar_dispositivos_paginados(db: Session, limit: int = 10, offset: int = 0):
        dispositivos = dispositivo_repository.find_all_paginate(db, limit, offset)
        return [DispositivoResponse.model_validate(dispositivo) for dispositivo in dispositivos]

    @staticmethod
    def buscar_dispositivo(db: Session, dispositivo_id: int):
        if dispositivo_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        dispositivo = dispositivo_repository.find_by_id(db, dispositivo_id)

        if not dispositivo:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.dispositivo_nao_encontrado"))

        return DispositivoResponse.model_validate(dispositivo)

    @staticmethod
    def excluir_dispositivo(db: Session, dispositivo_id: int):
        if dispositivo_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        dispositivo = dispositivo_repository.find_by_id(db, dispositivo_id)
        if not dispositivo:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.dispositivo_nao_encontrado"))

        try:
            dispositivo_repository.delete_by_id(db, dispositivo_id)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.dependencias"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        return True

    @staticmethod
    def atualizar_usuario(db: Session, dispositivo_schema: DispositivoUpdate) -> DispositivoResponse:
        dispositivo = dispositivo_repository.find_by_id(db, dispositivo_schema.id)
        if not dispositivo:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erros.dispositivo_nao_encontrado"))

        update_data = dispositivo_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(dispositivo, key, value)

        db.commit()
        db.refresh(dispositivo)
        return DispositivoResponse.model_validate(dispositivo)
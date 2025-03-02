"""
@author maria
date: 2025-02-25
"""

"""
@author maria
date: 2025-02-25
"""

from sqlalchemy.orm import Session
from app.schemas.unidade_medida_schema import UnidadeMedidaCreate, UnidadeMedidaResponse, UnidadeMedidaUpdate
from app.config import MessageLoader
from app.repositories.unidade_medida_repository import UnidadeMedidaRepository as unidade_medida_repository
from app.models.unidade_medida_model import UnidadeMedida
from sqlalchemy.exc import IntegrityError, DataError, InvalidRequestError, StatementError, DatabaseError
from fastapi import HTTPException

class UnidadeMedidaService:

    @staticmethod
    def criar_unidade(db: Session, unidade_medida_schema: UnidadeMedidaCreate) -> UnidadeMedidaResponse:
        if unidade_medida_schema is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        unidade_dict = unidade_medida_schema.model_dump()
        unidade_obj = UnidadeMedida(**unidade_dict)

        try:
            unidade_medida = unidade_medida_repository.save(db, unidade_obj)
        except DataError:  # campo grande
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.tamanho_dados"))
        except InvalidRequestError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.requisicao_invalida"))
        except StatementError:  # valor do enum inválido
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.valor_invalido"))
        except DatabaseError:
            db.rollback()
            raise HTTPException(status_code=500, detail=MessageLoader.get("erro.banco"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        unidade_response = UnidadeMedidaResponse.model_validate(unidade_medida, from_attributes=True)
        return unidade_response

    @staticmethod
    def listar_unidades(db: Session):
        unidades = unidade_medida_repository.find_all(db)
        return [UnidadeMedidaResponse.model_validate(unidade_medida) for unidade_medida in unidades]

    @staticmethod
    def listar_unidades_paginado(db: Session, limit: int = 10, offset: int = 0):
        unidades = unidade_medida_repository.find_all_paginate(db, limit, offset)
        return [UnidadeMedidaResponse.model_validate(unidade_medida) for unidade_medida in unidades]

    @staticmethod
    def buscar_unidade(db: Session, unidade_id: int):
        if unidade_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        unidade_medida = unidade_medida_repository.find_by_id(db, unidade_id)

        if not unidade_medida:
            msg = MessageLoader.get("erro.unidade_nao_encontrada")
            raise HTTPException(status_code=404, detail=msg)

        return UnidadeMedidaResponse.model_validate(unidade_medida)

    @staticmethod
    def excluir_unidade(db: Session, unidade_id: int):
        if unidade_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        unidade_medida = unidade_medida_repository.find_by_id(db, unidade_id)
        if not unidade_medida:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.unidade_nao_encontrada"))

        try:
            unidade_medida_repository.delete_by_id(db, unidade_id)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.dependencias"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        return True

    @staticmethod
    def atualizar_unidade(db: Session, unidade_medida_schema: UnidadeMedidaUpdate) -> UnidadeMedidaResponse:
        unidade_medida = unidade_medida_repository.find_by_id(db, unidade_medida_schema.id)
        if not unidade_medida:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.unidade_nao_encontrada"))

        update_data = unidade_medida_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(unidade_medida, key, value)

        db.commit()
        db.refresh(unidade_medida)
        return UnidadeMedidaResponse.model_validate(unidade_medida)
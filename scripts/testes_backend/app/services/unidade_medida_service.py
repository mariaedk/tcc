"""
@author maria
date: 2025-02-25
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.unidade_medida_schema import UnidadeMedidaCreate, UnidadeMedidaResponse, UnidadeMedidaUpdate
import app.repositories.unidade_medida_repository as unidade_repository
from app.config import MessageLoader

class UnidadeMedidaService:

    @staticmethod
    def criar_unidade_medida(db: Session, unidade_schema: UnidadeMedidaCreate) -> UnidadeMedidaResponse:
        if unidade_schema is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erros.parametro_nao_informado"))

        unidade_dict = unidade_schema.model_dump()
        unidade = unidade_repository.save(db, unidade_dict)
        return UnidadeMedidaResponse.model_validate(unidade)

    @staticmethod
    def listar_unidades_medida(db: Session):
        unidades = unidade_repository.find_all(db)
        return [UnidadeMedidaResponse.model_validate(unidade) for unidade in unidades]

    @staticmethod
    def buscar_unidade_medida(db: Session, unidade_id: int):
        if unidade_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erros.parametro_nao_informado"))

        unidade = unidade_repository.find_by_id(db, unidade_id)
        if not unidade:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erros.unidade_nao_encontrada"))

        return UnidadeMedidaResponse.model_validate(unidade)

    @staticmethod
    def excluir_unidade_medida(db: Session, unidade_id: int):
        if unidade_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erros.parametro_nao_informado"))

        unidade = unidade_repository.find_by_id(db, unidade_id)
        if not unidade:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erros.unidade_nao_encontrada"))

        unidade_repository.delete_by_id(db, unidade_id)
        return {"message": "Unidade de medida excluída com sucesso"}

    @staticmethod
    def atualizar_unidade_medida(db: Session, unidade_schema: UnidadeMedidaUpdate) -> UnidadeMedidaResponse:
        unidade = unidade_repository.find_by_id(db, unidade_schema.id)
        if not unidade:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erros.unidade_nao_encontrada"))

        update_data = unidade_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(unidade, key, value)

        db.commit()
        db.refresh(unidade)
        return UnidadeMedidaResponse.model_validate(unidade)

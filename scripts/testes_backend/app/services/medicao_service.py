"""
@author maria
date: 2025-02-27
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.medicao_schema import MedicaoCreate, MedicaoResponse, MedicaoUpdate
import app.repositories.medicao_repository as medicao_repository
from app.config import MessageLoader

class MedicaoService:

    @staticmethod
    def criar_medicao(db: Session, medicao_schema: MedicaoCreate) -> MedicaoResponse:
        if medicao_schema is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erros.parametro_nao_informado"))

        medicao_dict = medicao_schema.model_dump()
        medicao = medicao_repository.save(db, medicao_dict)
        return MedicaoResponse.model_validate(medicao)

    @staticmethod
    def listar_medicoes(db: Session):
        medicoes = medicao_repository.find_all(db)
        return [MedicaoResponse.model_validate(medicao) for medicao in medicoes]

    @staticmethod
    def buscar_medicao(db: Session, medicao_id: int):
        if medicao_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erros.parametro_nao_informado"))

        medicao = medicao_repository.find_by_id(db, medicao_id)
        if not medicao:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erros.medicao_nao_encontrada"))

        return MedicaoResponse.model_validate(medicao)

    @staticmethod
    def excluir_medicao(db: Session, medicao_id: int):
        if medicao_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erros.parametro_nao_informado"))

        medicao = medicao_repository.find_by_id(db, medicao_id)
        if not medicao:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erros.medicao_nao_encontrada"))

        medicao_repository.delete_by_id(db, medicao_id)
        return {"message": "Medição excluída com sucesso"}

    @staticmethod
    def atualizar_medicao(db: Session, medicao_schema: MedicaoUpdate) -> MedicaoResponse:
        medicao = medicao_repository.find_by_id(db, medicao_schema.id)
        if not medicao:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erros.medicao_nao_encontrada"))

        update_data = medicao_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(medicao, key, value)

        db.commit()
        db.refresh(medicao)
        return MedicaoResponse.model_validate(medicao)

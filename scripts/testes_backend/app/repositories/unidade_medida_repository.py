"""
@author maria
date: 2025-02-25
"""

from sqlalchemy.orm import Session
from app.models.unidade_medida_model import UnidadeMedida

class UnidadeMedidaRepository:

    @staticmethod
    def find_all(db: Session) -> list[UnidadeMedida]:
        return db.query(UnidadeMedida).all()

    @staticmethod
    def find_all_paginate(db: Session, limit: int = 10, offset: int = 0):
        return db.query(UnidadeMedida).offset(offset).limit(limit).all()

    @staticmethod
    def save(db: Session, unidade_medida: UnidadeMedida) -> UnidadeMedida:
        if unidade_medida.id:
            db.merge(unidade_medida)
        else:
            db.add(unidade_medida)
        db.commit()
        db.refresh(unidade_medida)
        return unidade_medida

    @staticmethod
    def find_by_id(db: Session, id: int) -> UnidadeMedida | None:
        return db.query(UnidadeMedida).filter(UnidadeMedida.id == id).first()

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        unidade_medida = db.query(UnidadeMedida).filter(UnidadeMedida.id == id).first()
        if unidade_medida:
            db.delete(unidade_medida)
            db.commit()
"""
@author maria
date: 2025-04-17
"""

from sqlalchemy.orm import Session
from app.models.coleta_model import Coleta

class ColetaRepository:

    @staticmethod
    def save(db: Session, coleta: Coleta) -> Coleta:
        db.add(coleta)
        db.commit()
        db.refresh(coleta)
        return coleta

    @staticmethod
    def find_by_id(db: Session, id: int) -> Coleta | None:
        return db.query(Coleta).filter(Coleta.id == id).first()

    @staticmethod
    def find_all(db: Session) -> list[Coleta]:
        return db.query(Coleta).all()

    @staticmethod
    def find_all_paginate(db: Session, limit: int = 10, offset: int = 0):
        return db.query(Coleta).offset(offset).limit(limit).all()

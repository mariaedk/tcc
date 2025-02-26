"""Dispositivo
@author maria
date: 2025-02-25
"""

from sqlalchemy.orm import Session
from app.models.dispositivo_model import Dispositivo

class DispositivoRepository:

    @staticmethod
    def find_all(db: Session) -> list[Dispositivo]:
        return db.query(Dispositivo).all()

    @staticmethod
    def find_all_paginate(db: Session, limit: int = 10, offset: int = 0):
        return db.query(Dispositivo).offset(offset).limit(limit).all()

    @staticmethod
    def save(db: Session, dispositivo: Dispositivo) -> Dispositivo:
        if dispositivo.id:
            db.merge(dispositivo)
        else:
            db.add(dispositivo)
        db.commit()
        db.refresh(dispositivo)
        return dispositivo

    @staticmethod
    def find_by_id(db: Session, id: int) -> Dispositivo | None:
        return db.query(Dispositivo).filter(Dispositivo.id == id).first()

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        dispositivo = db.query(Dispositivo).filter(Dispositivo.id == id).first()
        if dispositivo:
            db.delete(dispositivo)
            db.commit()
"""
@author maria
date: 2025-02-24
"""

from sqlalchemy.orm import Session
from app.models.usuario_model import Usuario

class UsuarioRepository:

    @staticmethod
    def find_all(db: Session) -> list[Usuario]:
        return db.query(Usuario).all()

    @staticmethod
    def find_all_paginate(db: Session, limit: int = 10, offset: int = 0):
        return db.query(Usuario).offset(offset).limit(limit).all()

    @staticmethod
    def save(db: Session, usuario: Usuario) -> Usuario:
        if usuario.id:
            db.merge(usuario)
        else:
            db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def find_by_id(db: Session, id: int) -> Usuario | None:
        return db.query(Usuario).filter(Usuario.id == id).first()

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if usuario:
            db.delete(usuario)
            db.commit()
"""
@author maria
date: 2025-02-25
"""

from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
import app.repositories.usuario_repository as usuario_repository
import bcrypt

class UsuarioService:

    @staticmethod
    def criar_usuario(db: Session, usuario_schema: UsuarioCreate) -> UsuarioResponse:
        senha_hash = bcrypt.hashpw(usuario_schema.senha.encode(), bcrypt.gensalt()).decode()

        usuario_dict = usuario_schema.dict()
        usuario_dict["senha"] = senha_hash

        usuario = usuario_repository.save(db, usuario_dict)
        return UsuarioResponse.from_orm(usuario)

    @staticmethod
    def listar_usuarios(db: Session):
        usuarios = usuario_repository.find_all(db)
        return [UsuarioResponse.from_orm(usuario) for usuario in usuarios]

    @staticmethod
    def listar_usuarios_paginados(db: Session, limit: int = 10, offset: int = 0):
        usuarios = usuario_repository.find_all_paginate(db, limit, offset)
        return [UsuarioResponse.from_orm(usuario) for usuario in usuarios]

    @staticmethod
    def buscar_usuario(db: Session, usuario_id: int):
        usuario = usuario_repository.find_by_id(db, usuario_id)
        return UsuarioResponse.from_orm(usuario) if usuario else None

    @staticmethod
    def excluir_usuario(db: Session, usuario_id: int):
        usuario = usuario_repository.delete_by_id(db, usuario_id)
        return usuario is not None
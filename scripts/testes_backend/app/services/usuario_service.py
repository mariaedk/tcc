"""
@author maria
date: 2025-02-25
"""

from sqlalchemy.orm import Session
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.config import MessageLoader
from app.repositories.usuario_repository import UsuarioRepository as usuario_repository
from app.models.usuario_model import Usuario
from sqlalchemy.exc import IntegrityError, DataError, InvalidRequestError, StatementError, DatabaseError
from fastapi import HTTPException
import bcrypt

class UsuarioService:

    @staticmethod
    def criar_usuario(db: Session, usuario_schema: UsuarioCreate) -> UsuarioResponse:
        if usuario_schema is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        senha_hash = bcrypt.hashpw(usuario_schema.senha.encode(), bcrypt.gensalt()).decode()

        usuario_dict = usuario_schema.model_dump()
        usuario_dict["senha"] = senha_hash

        usuario_obj = Usuario(**usuario_dict)
        try:
            usuario = usuario_repository.save(db, usuario_obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.chave_duplicada"))
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

        usuario_response = UsuarioResponse.model_validate(usuario, from_attributes=True)
        return usuario_response

    @staticmethod
    def listar_usuarios(db: Session):
        usuarios = usuario_repository.find_all(db)
        return [UsuarioResponse.model_validate(usuario) for usuario in usuarios]

    @staticmethod
    def listar_usuarios_paginados(db: Session, limit: int = 10, offset: int = 0):
        usuarios = usuario_repository.find_all_paginate(db, limit, offset)
        return [UsuarioResponse.model_validate(usuario) for usuario in usuarios]

    @staticmethod
    def buscar_usuario(db: Session, usuario_id: int):
        if usuario_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        usuario = usuario_repository.find_by_id(db, usuario_id)

        if not usuario:
            msg = MessageLoader.get("erro.usuario_nao_encontrado")
            raise HTTPException(status_code=404, detail=msg)

        return UsuarioResponse.model_validate(usuario)

    @staticmethod
    def excluir_usuario(db: Session, usuario_id: int):
        if usuario_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        usuario = usuario_repository.find_by_id(db, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.usuario_nao_encontrado"))

        try:
            usuario_repository.delete_by_id(db, usuario_id)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.dependencias"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        return True

    @staticmethod
    def atualizar_usuario(db: Session, usuario_schema: UsuarioUpdate) -> UsuarioResponse:
        usuario = usuario_repository.find_by_id(db, usuario_schema.id)
        if not usuario:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.usuario_nao_encontrado"))

        update_data = usuario_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(usuario, key, value)

        usuario = usuario_repository.update(db, usuario)
        return UsuarioResponse.model_validate(usuario)
"""
@author maria
date: 2025-02-24
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services.usuario_service import UsuarioService

usuario_router = APIRouter()
usuario_service = UsuarioService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@usuario_router.post("/usuarios", response_model=UsuarioResponse)
def criar_usuario(usuario_schema: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.criar_usuario(db, usuario_schema)

@usuario_router.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.listar_usuarios(db)

@usuario_router.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios_paginados(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return usuario_service.listar_usuarios_paginados(db, limit, offset)

@usuario_router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return usuario_service.buscar_usuario(db, usuario_id)

@usuario_router.delete("/usuarios/{usuario_id}")
def excluir_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return usuario_service.excluir_usuario(db, usuario_id)

@usuario_router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(usuario_schema: UsuarioUpdate, db: Session = Depends(get_db)):
    return UsuarioService.atualizar_usuario(db, usuario_schema)

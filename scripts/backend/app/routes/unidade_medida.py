"""
@author maria
date: 2025-03-02
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.unidade_medida_schema import UnidadeMedidaCreate, UnidadeMedidaResponse, UnidadeMedidaUpdate
from app.services.unidade_medida_service import UnidadeMedidaService
from app.services.auth import get_current_user

unidade_router = APIRouter(prefix="/unidade-medida", tags=["Unidade de Medida"], dependencies=[Depends(get_current_user)])
unidade_service = UnidadeMedidaService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@unidade_router.post("", response_model=UnidadeMedidaResponse)
def criar_unidade_medida(unidade_medida_schema: UnidadeMedidaCreate, db: Session = Depends(get_db)):
    return unidade_service.criar_unidade(db, unidade_medida_schema)

@unidade_router.get("/all", response_model=list[UnidadeMedidaResponse])
def listar_unidade_medida(db: Session = Depends(get_db)):
    return unidade_service.listar_unidades(db)

@unidade_router.get("", response_model=list[UnidadeMedidaResponse])
def listar_unidade_medida_paginado(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return unidade_service.listar_unidades_paginado(db, limit, offset)

@unidade_router.get("/{id}", response_model=UnidadeMedidaResponse)
def buscar_unidade_medida(id: int, db: Session = Depends(get_db)):
    return unidade_service.buscar_unidade(db, id)

@unidade_router.delete("/{id}")
def excluir_unidade_medida(id: int, db: Session = Depends(get_db)):
    return unidade_service.excluir_unidade(db, id)

@unidade_router.put("", response_model=UnidadeMedidaResponse)
def atualizar_unidade_medida(unidade_medida_schema: UnidadeMedidaUpdate, db: Session = Depends(get_db)):
    return unidade_service.atualizar_unidade(db, unidade_medida_schema)
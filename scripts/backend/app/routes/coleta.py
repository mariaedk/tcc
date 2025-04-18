"""
@author maria
date: 2025-04-17
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.coleta_service import ColetaService
from app.schemas.coleta_schema import ColetaCreate, ColetaResponse
from app.services.auth import get_current_user

coleta_router = APIRouter(prefix="/coleta", tags=["Coletas"], dependencies=[Depends(get_current_user)])
coleta_service = ColetaService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@coleta_router.post("", response_model=ColetaResponse)
def criar_coleta(coleta_schema: ColetaCreate, db: Session = Depends(get_db)):
    return coleta_service.criar_coleta(db, coleta_schema)

@coleta_router.get("/all", response_model=list[ColetaResponse])
def listar_coletas(db: Session = Depends(get_db)):
    return coleta_service.listar_coletas(db)

@coleta_router.get("", response_model=list[ColetaResponse])
def listar_coletas_paginadas(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return coleta_service.listar_coletas_paginadas(db, limit, offset)

@coleta_router.get("/{coleta_id}", response_model=ColetaResponse)
def buscar_coleta(coleta_id: int, db: Session = Depends(get_db)):
    return coleta_service.buscar_coleta(db, coleta_id)

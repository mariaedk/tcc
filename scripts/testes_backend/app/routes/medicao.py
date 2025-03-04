"""
@author maria
date: 2025-03-04
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.medicao_schema import MedicaoCreate, MedicaoResponse
from app.services.medicao_service import MedicaoService

medicao_router = APIRouter(prefix="/medicao", tags=["Medições"])
medicao_service = MedicaoService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@medicao_router.post("", response_model=MedicaoResponse)
def criar_medicao(medicao_schema: MedicaoCreate, db: Session = Depends(get_db)):
    return medicao_service.criar_medicao(db, medicao_schema)

@medicao_router.get("/all", response_model=list[MedicaoResponse])
def listar_medicao(db: Session = Depends(get_db)):
    return medicao_service.listar_medicoes(db)

@medicao_router.get("", response_model=list[MedicaoResponse])
def listar_medicaos_paginados(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return medicao_service.listar_medicoes_paginadas(db, limit, offset)

@medicao_router.get("/{medicao_id}", response_model=MedicaoResponse)
def buscar_medicao(medicao_id: int, db: Session = Depends(get_db)):
    return medicao_service.buscar_medicao(db, medicao_id)
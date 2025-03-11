"""
@author maria
date: 2025-03-02
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.dispositivo_schema import DispositivoCreate, DispositivoResponse, DispositivoUpdate
from app.services.dispositivo_service import DispositivoService

dispositivo_router = APIRouter(prefix="/dispositivo", tags=["Dispositivos"])
dispositivo_service = DispositivoService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@dispositivo_router.post("", response_model=DispositivoResponse)
def criar_dispositivo(dispositivo_schema: DispositivoCreate, db: Session = Depends(get_db)):
    return dispositivo_service.criar_dispositivo(db, dispositivo_schema)

@dispositivo_router.get("/all", response_model=list[DispositivoResponse])
def listar_dispositivos(db: Session = Depends(get_db)):
    return dispositivo_service.listar_dispositivos(db)

@dispositivo_router.get("", response_model=list[DispositivoResponse])
def listar_dispositivos_paginados(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return dispositivo_service.listar_dispositivos_paginados(db, limit, offset)

@dispositivo_router.get("/{dispositivo_id}", response_model=DispositivoResponse)
def buscar_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    return dispositivo_service.buscar_dispositivo(db, dispositivo_id)

@dispositivo_router.delete("/{dispositivo_id}")
def excluir_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    return dispositivo_service.excluir_dispositivo(db, dispositivo_id)

@dispositivo_router.put("/{dispositivo_id}", response_model=DispositivoResponse)
def atualizar_dispositivo(dispositivo_schema: DispositivoUpdate, db: Session = Depends(get_db)):
    return dispositivo_service.atualizar_dispositivo(db, dispositivo_schema)

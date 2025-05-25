"""
@author maria
date: 2025-03-04
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.medicao_schema import MedicaoCreate, MedicaoResponse, MedicaoHistoricoSchema
from app.services.medicao_service import MedicaoService
from app.services.auth import get_current_user

medicao_router = APIRouter(prefix="/medicao", tags=["Medições"], dependencies=[Depends(get_current_user)])
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

@medicao_router.get("/media-por-hora/{sensor_codigo}", response_model=list[MedicaoHistoricoSchema])
def listar_medicoes_por_hora(
    sensor_codigo: int,
    data: datetime = Query(None),
    db: Session = Depends(get_db)
):
    return medicao_service.buscar_medicoes_por_hora(db, sensor_codigo, data)

@medicao_router.get("/media-por-dia/{sensor_codigo}", response_model=list[MedicaoHistoricoSchema])
def listar_medicoes_media_por_dia(
    sensor_codigo: int,
    data: datetime = Query(None),
    data_inicio: datetime = Query(None),
    data_fim: datetime = Query(None),
    dias: int = Query(None),
    db: Session = Depends(get_db)
):
    return medicao_service.buscar_medicoes_media_por_dia(db, sensor_codigo, data, data_inicio, data_fim, dias)

@medicao_router.get("/historico/{sensor_codigo}", response_model=list[MedicaoHistoricoSchema])
def obter_historico_medicoes(
    sensor_codigo: int,
    tipo: str,
    data: Optional[datetime] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    dias: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    return MedicaoService.buscar_medicoes(
        db=db,
        sensor_codigo=sensor_codigo,
        tipo=tipo,
        data=data,
        data_inicio=data_inicio,
        data_fim=data_fim,
        dias=dias
    )

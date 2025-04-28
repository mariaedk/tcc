"""
@author maria
date: 2025-03-04
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.medicao_schema import MedicaoCreate, MedicaoResponse, MedicaoHistoricoSchema, ComparativoVazaoResponseSchema
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

@medicao_router.get("/historico-data/sensor/{cd_sensor}/{dias}", response_model=list[MedicaoHistoricoSchema])
def historico_medicoes(cd_sensor: int, dias: int = 30, db: Session = Depends(get_db)):
    return medicao_service.obter_historico_por_sensor(db, cd_sensor, dias)

@medicao_router.get("/data", response_model=list[MedicaoHistoricoSchema])
def buscar_por_data(data: datetime = Query(...), db: Session = Depends(get_db)):
    return MedicaoService.buscar_por_data(db, data)

@medicao_router.get("/intervalo_datas", response_model=list[MedicaoHistoricoSchema])
def buscar_por_intervalo_datas(
    data_inicio: datetime = Query(...),
    data_fim: datetime = Query(...),
    db: Session = Depends(get_db)
):
    return MedicaoService.buscar_por_intervalo_datas(db, data_inicio, data_fim)

@medicao_router.get("/vazoes-mes/{codigo_entrada}/{codigo_saida}")
def comparar_vazoes_por_mes(
    codigo_entrada: int,
    codigo_saida: int,
    meses: Optional[int] = 6,
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    return MedicaoService.comparar_vazoes_por_mes(
        db=db,
        codigo_entrada=codigo_entrada,
        codigo_saida=codigo_saida,
        meses=meses,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

@medicao_router.get("/geral/{sensor_codigo}", response_model=list[MedicaoResponse])
def listar_medicoes_geral(
    sensor_codigo: int,
    data: datetime = Query(None),
    data_inicio: datetime = Query(None),
    data_fim: datetime = Query(None),
    dias: int = Query(None),
    db: Session = Depends(get_db)
):
    return medicao_service.buscar_medicoes_geral(db, sensor_codigo, data, data_inicio, data_fim, dias)

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

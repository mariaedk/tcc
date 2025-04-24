"""
@author maria
date: 2025-03-04
"""
from datetime import datetime

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

@medicao_router.get("/historico-data/dispositivo/{cd_dispositivo}", response_model=list[MedicaoHistoricoSchema])
def historico_medicoes(cd_dispositivo: int, dias: int = 30, db: Session = Depends(get_db)):
    return medicao_service.obter_historico_por_sensor(db, cd_dispositivo, dias)

@medicao_router.get("/sensor/{sensor_id}", response_model=list[MedicaoResponse])
def buscar_por_sensor(sensor_id: int, db: Session = Depends(get_db)):
    return MedicaoService.buscar_por_sensor(db, sensor_id)

@medicao_router.get("/coleta/{coleta_id}", response_model=list[MedicaoResponse])
def buscar_por_coleta(coleta_id: int, db: Session = Depends(get_db)):
    return MedicaoService.buscar_por_coleta(db, coleta_id)

@medicao_router.get("/unidade/{unidade_id}", response_model=list[MedicaoResponse])
def buscar_por_unidade(unidade_id: int, db: Session = Depends(get_db)):
    return MedicaoService.buscar_por_unidade(db, unidade_id)

@medicao_router.get("/data_inicio", response_model=list[MedicaoResponse])
def buscar_por_data_inicio(data: datetime = Query(...), db: Session = Depends(get_db)):
    return MedicaoService.buscar_por_data_inicio(db, data)

@medicao_router.get("/data_fim", response_model=list[MedicaoResponse])
def buscar_por_data_fim(data: datetime = Query(...), db: Session = Depends(get_db)):
    return MedicaoService.buscar_por_data_fim(db, data)

@medicao_router.get("/intervalo_datas", response_model=list[MedicaoResponse])
def buscar_por_intervalo_datas(
    data_inicio: datetime = Query(...),
    data_fim: datetime = Query(...),
    db: Session = Depends(get_db)
):
    return MedicaoService.buscar_por_intervalo_datas(db, data_inicio, data_fim)

@medicao_router.get("/vazoes-dia/{cd_sensor_entrada}/{cd_sensor_saida}/{dias}", response_model=ComparativoVazaoResponseSchema)
def comparar_vazoes_por_dia(cd_sensor_entrada: int, cd_sensor_saida: int, dias: int = 7, db: Session = Depends(get_db)):
    return medicao_service.comparar_vazoes_por_dia(db, cd_sensor_entrada, cd_sensor_saida, dias)
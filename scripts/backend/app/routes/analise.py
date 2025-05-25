"""
@author maria
date: 2025-04-22
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.auth import get_current_user
from app.services.medicao_service import MedicaoService as medicao_service
from analise.services.analise_nivel_service import AnaliseNivelService
from app.models.enums import TipoMedicao

analise_router = APIRouter(prefix="/analise", tags=["Análise Automática"], dependencies=[Depends(get_current_user)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@analise_router.get("/nivel/sensor/{cd_sensor}")
def analisar_nivel_sensor(
    cd_sensor: int,
    tipo: TipoMedicao,
    dias: Optional[int] = Query(None),
    data: Optional[datetime] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    service = AnaliseNivelService()
    medicoes = medicao_service.buscar_medicoes(
        db, cd_sensor, data=data, data_inicio=data_inicio, data_fim=data_fim, dias=dias, tipo=tipo)

    return service.analisar(
        medicoes,
        sensor_codigo=cd_sensor,
        tipo=tipo,
        data=data,
        data_inicio=data_inicio,
        data_fim=data_fim,
        dias=dias
    )


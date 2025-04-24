"""
@author maria
date: 2025-04-22
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.auth import get_current_user
from app.repositories.medicao_repository import MedicaoRepository as medicao_repository
from analise.services.analise_nivel_service import AnaliseNivelService

analise_router = APIRouter(prefix="/analise", tags=["Análise Automática"], dependencies=[Depends(get_current_user)])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@analise_router.get("/nivel/sensor/{cd_sensor}")
def analisar_nivel_sensor(cd_sensor: int, dias: int = 7, db: Session = Depends(get_db)):
    medicoes = medicao_repository.media_por_dia_por_sensor(db, cd_sensor, dias)
    service = AnaliseNivelService(dias)
    resp = service.analisar(medicoes, cd_sensor)
    return resp

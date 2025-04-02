"""
@author maria
date: 2025-03-04
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.sensor_schema import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import SensorService
from app.services.auth import get_current_user

sensor_router = APIRouter(prefix="/sensor", tags=["Sensores"], dependencies=[Depends(get_current_user)])
sensor_service = SensorService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@sensor_router.post("", response_model=SensorResponse)
def criar_sensor(sensor_schema: SensorCreate, db: Session = Depends(get_db)):
    return sensor_service.criar_sensor(db, sensor_schema)

@sensor_router.get("/all", response_model=list[SensorResponse])
def listar_sensores(db: Session = Depends(get_db)):
    return sensor_service.listar_sensores(db)

@sensor_router.get("", response_model=list[SensorResponse])
def listar_sensores_paginados(db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    return sensor_service.listar_sensores_paginados(db, limit, offset)

@sensor_router.get("/{sensor_id}", response_model=SensorResponse)
def buscar_sensor(sensor_id: int, db: Session = Depends(get_db)):
    return sensor_service.buscar_sensor(db, sensor_id)

@sensor_router.delete("/{sensor_id}")
def excluir_sensor(sensor_id: int, db: Session = Depends(get_db)):
    return sensor_service.excluir_sensor(db, sensor_id)

@sensor_router.put("/{sensor_id}", response_model=SensorResponse)
def atualizar_sensor(sensor_schema: SensorUpdate, db: Session = Depends(get_db)):
    return sensor_service.atualizar_sensor(db, sensor_schema)

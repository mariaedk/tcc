"""
@author maria
date: 2025-05-03
"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.enums import TipoMedicao
from app.database import SessionLocal
from app.services.auth import get_current_user
from app.services.export.report_service import ReportService

report_router = APIRouter(prefix="/report", tags=["Relatórios"], dependencies=[Depends(get_current_user)])
report_service = ReportService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Report:

    @report_router.get("/nivel/export/xls")
    def get_nivel_export_xls(sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                             data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None, db: Session = Depends(get_db)):
        return ReportService.get_nivel_export_xls(db, sensor_codigo, data, data_inicio, data_fim, dias, tipo_medicao)

    @report_router.get("/vazao/export/xls")
    def get_vazao_export_xls(sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                             data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None, db: Session = Depends(get_db)):
        return ReportService.get_vazao_export_xls(db, sensor_codigo, data, data_inicio, data_fim, dias, tipo_medicao)

    @report_router.get("/analise/anomalia/export/xls")
    def get_analise_anomalias_export_xls(sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                             data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None, db: Session = Depends(get_db)):
        return ReportService.get_analise_anomalias_export_xls(db, sensor_codigo, data, data_inicio, data_fim, dias, tipo_medicao)

    @report_router.get("/nivel/export/pdf")
    def exportar_pdf_nivel(sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                             data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None, db: Session = Depends(get_db)):
        return ReportService.get_nivel_export_pdf(db, sensor_codigo, data, data_inicio, data_fim, dias, tipo_medicao)

    @report_router.get("/vazao/export/pdf")
    def exportar_pdf_nivel(sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                             data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None, db: Session = Depends(get_db)):
        return ReportService.get_vazao_export_pdf(db, sensor_codigo, data, data_inicio, data_fim, dias, tipo_medicao)

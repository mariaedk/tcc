"""
@author maria
date: 2025-05-03
"""
from datetime import datetime
from fastapi import HTTPException

from analise.services.analise_nivel_service import AnaliseNivelService
from app.config.messages import MessageLoader
from sqlalchemy.orm import Session
from app.models.enums import TipoMedicao
from app.services.export.xls import AnomaliasExport
from app.services.medicao_service import MedicaoService
from app.services.export.xls.nivel_export import NivelExport
from app.services.export.xls.vazao_export import VazaoExport

class ReportService:

    @staticmethod
    def get_nivel_export_xls(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                             data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):
        if not sensor_codigo:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        if tipo_medicao == TipoMedicao.DIA:
            medicoes = MedicaoService.buscar_medicoes_media_por_dia(db, sensor_codigo, data, data_inicio, data_fim,
                                                                    dias)
        else:
            medicoes = MedicaoService.buscar_medicoes_por_hora(db, sensor_codigo, data)

        filtros = {
            "Data": data.strftime('%d/%m/%Y') if data else None,
            "Data Início": data_inicio.strftime('%d/%m/%Y') if data_inicio else None,
            "Data Fim": data_fim.strftime('%d/%m/%Y') if data_fim else None,
            "Dias": dias,
            "Tipo de Medição": tipo_medicao.value if tipo_medicao else None
        }

        exportador = NivelExport(medicoes, filtros)
        return exportador.gerar_excel()

    @staticmethod
    def get_vazao_export_xls(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                             data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):
        if not sensor_codigo:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        if tipo_medicao == TipoMedicao.DIA:
            medicoes = MedicaoService.buscar_medicoes_media_por_dia(db, sensor_codigo, data, data_inicio, data_fim,
                                                                    dias)
        else:
            medicoes = MedicaoService.buscar_medicoes_por_hora(db, sensor_codigo, data)

        filtros = {
            "Data": data.strftime('%d/%m/%Y') if data else None,
            "Data Início": data_inicio.strftime('%d/%m/%Y') if data_inicio else None,
            "Data Fim": data_fim.strftime('%d/%m/%Y') if data_fim else None,
            "Dias": dias,
            "Tipo de Medição": tipo_medicao.value if tipo_medicao else None
        }

        exportador = VazaoExport(medicoes, filtros)
        return exportador.gerar_excel()

    @staticmethod
    def get_analise_anomalias_export_xls(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                             data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):
        if not sensor_codigo:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        if tipo_medicao == TipoMedicao.DIA:
            medicoes = MedicaoService.buscar_medicoes_media_por_dia(db, sensor_codigo, data, data_inicio, data_fim,
                                                                    dias)
        else:
            medicoes = MedicaoService.buscar_medicoes_por_hora(db, sensor_codigo, data)

        service = AnaliseNivelService()
        resultado = service.analisar(medicoes, sensor_codigo, tipo=tipo_medicao, data=data, data_inicio=data_inicio, data_fim=data_fim, dias=dias)

        filtros = {
            "Data": data.strftime('%d/%m/%Y') if data else None,
            "Data Início": data_inicio.strftime('%d/%m/%Y') if data_inicio else None,
            "Data Fim": data_fim.strftime('%d/%m/%Y') if data_fim else None,
            "Dias": dias,
            "Tipo de Medição": tipo_medicao.value if tipo_medicao else None
        }

        exportador = AnomaliasExport(resultado, filtros)
        return exportador.gerar_excel()
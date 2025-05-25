"""
@author maria
date: 2025-05-03
"""
from datetime import datetime
from fastapi import HTTPException
from jinja2 import Template
from weasyprint import HTML
from fastapi.responses import Response
from analise.services.analise_nivel_service import AnaliseNivelService
from app.config.messages import MessageLoader
from sqlalchemy.orm import Session
from app.models.enums import TipoMedicao
from app.services.medicao_service import MedicaoService
from app.services.export.grafico_service import GraficoService
from pytz import timezone
from app.services.export.xls.vazao_export import VazaoExport
from app.services.export.xls.nivel_export import NivelExport
from app.services.export.xls.analise_anomalias_export import AnomaliasExport
import os


class ReportService:

    @staticmethod
    def __buscar_medicoes(db: Session, sensor_codigo: int, tipo_medicao: TipoMedicao,
                           data: datetime = None, data_inicio: datetime = None,
                           data_fim: datetime = None, dias: int = None):
        if not sensor_codigo:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        return MedicaoService.buscar_medicoes(
            db,
            sensor_codigo=sensor_codigo,
            tipo=tipo_medicao,
            data=data,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dias=dias
        )

    @staticmethod
    def __gerar_filtros(tipo_medicao, data, data_inicio, data_fim, dias):
        return {
            "Tipo de Medição": tipo_medicao.value if tipo_medicao else "-",
            "Data": data.strftime('%d/%m/%Y') if data else "-",
            "Data Início": data_inicio.strftime('%d/%m/%Y') if data_inicio else "-",
            "Data Fim": data_fim.strftime('%d/%m/%Y') if data_fim else "-",
            "Dias": dias if dias is not None else "-"
        }

    @staticmethod
    def get_nivel_export_pdf(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                              data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):

        medicoes = ReportService.__buscar_medicoes(db, sensor_codigo, tipo_medicao, data, data_inicio, data_fim, dias)

        filtros = ReportService.__gerar_filtros(tipo_medicao, data, data_inicio, data_fim, dias)

        template_path = os.path.join(os.path.dirname(__file__), "pdf", "nivel_relatorio.html")
        with open(template_path, "r", encoding="utf-8") as file:
            template = Template(file.read())

        imagem_base64 = GraficoService.gerar_grafico_base64(medicoes, tipo_medicao, "Relatório de Nível")

        fuso = timezone("America/Sao_Paulo")
        data_geracao = datetime.now(fuso).strftime("%d/%m/%Y %H:%M")

        html_renderizado = template.render(
            titulo="Relatório de Nível",
            data_geracao=data_geracao,
            filtros=filtros,
            dados=medicoes,
            imagem_base64=imagem_base64,
            tipo_medicao=tipo_medicao.name if tipo_medicao else "INST"
        )

        pdf = HTML(string=html_renderizado).write_pdf()

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="relatorio_nivel_{datetime.now(fuso).strftime("%Y%m%d_%H%M%S")}.pdf"'
            }
        )

    @staticmethod
    def get_vazao_export_pdf(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                              data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):

        medicoes = ReportService.__buscar_medicoes(db, sensor_codigo, tipo_medicao, data, data_inicio, data_fim, dias)

        filtros = ReportService.__gerar_filtros(tipo_medicao, data, data_inicio, data_fim, dias)

        template_path = os.path.join(os.path.dirname(__file__), "pdf", "vazao_relatorio.html")
        with open(template_path, "r", encoding="utf-8") as file:
            template = Template(file.read())

        imagem_base64 = GraficoService.gerar_grafico_base64(
            medicoes,
            tipo_medicao,
            titulo_grafico="Evolução da Vazão",
        )

        fuso = timezone("America/Sao_Paulo")
        data_geracao = datetime.now(fuso).strftime("%d/%m/%Y %H:%M")

        html_renderizado = template.render(
            titulo="Relatório de Vazão",
            data_geracao=data_geracao,
            filtros=filtros,
            dados=medicoes,
            imagem_base64=imagem_base64,
            tipo_medicao=tipo_medicao.name if tipo_medicao else "INST"
        )

        pdf = HTML(string=html_renderizado).write_pdf()

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="relatorio_vazao_{datetime.now(fuso).strftime("%Y%m%d_%H%M%S")}.pdf"'
            }
        )

    @staticmethod
    def get_anomalia_export_pdf(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                                data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):

        medicoes = ReportService.__buscar_medicoes(db, sensor_codigo, tipo_medicao, data, data_inicio, data_fim, dias)

        resultado = AnaliseNivelService().analisar(
            medicoes,
            sensor_codigo=sensor_codigo,
            tipo=tipo_medicao,
            data=data,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dias=dias
        )

        filtros = ReportService.__gerar_filtros(tipo_medicao, data, data_inicio, data_fim, dias)

        template_path = os.path.join(os.path.dirname(__file__), "pdf", "anomalia_relatorio.html")
        with open(template_path, "r", encoding="utf-8") as file:
            template = Template(file.read())

        imagem_base64 = GraficoService.gerar_grafico_base64(
            resultado.dados,
            tipo_medicao,
            titulo_grafico="Análise de Anomalias"
        )

        fuso = timezone("America/Sao_Paulo")
        data_geracao = datetime.now(fuso).strftime("%d/%m/%Y %H:%M")

        html_renderizado = template.render(
            titulo="Relatório de Análise de Anomalias",
            data_geracao=data_geracao,
            filtros=filtros,
            dados=resultado.dados,
            imagem_base64=imagem_base64,
            tipo_medicao=tipo_medicao.name if tipo_medicao else "INST",
            total_anomalias=resultado.anomalias,
            mensagem=resultado.mensagem
        )

        pdf = HTML(string=html_renderizado).write_pdf()

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="relatorio_anomalias_{datetime.now(fuso).strftime("%Y%m%d_%H%M%S")}.pdf"'
            }
        )

    @staticmethod
    def get_nivel_export_xls(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                              data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):

        medicoes = ReportService.__buscar_medicoes(db, sensor_codigo, tipo_medicao, data, data_inicio, data_fim, dias)

        filtros = ReportService.__gerar_filtros(tipo_medicao, data, data_inicio, data_fim, dias)

        exportador = NivelExport(medicoes, tipo_medicao, filtros)
        return exportador.gerar_excel()

    @staticmethod
    def get_vazao_export_xls(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                              data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):

        medicoes = ReportService.__buscar_medicoes(db, sensor_codigo, tipo_medicao, data, data_inicio, data_fim, dias)

        filtros = ReportService.__gerar_filtros(tipo_medicao, data, data_inicio, data_fim, dias)

        exportador = VazaoExport(medicoes, tipo_medicao, filtros)
        return exportador.gerar_excel()

    @staticmethod
    def get_analise_anomalias_export_xls(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                                          data_fim: datetime = None, dias: int = None, tipo_medicao: TipoMedicao = None):

        medicoes = ReportService.__buscar_medicoes(db, sensor_codigo, tipo_medicao, data, data_inicio, data_fim, dias)

        resultado = AnaliseNivelService().analisar(
            medicoes,
            sensor_codigo=sensor_codigo,
            tipo=tipo_medicao,
            data=data,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dias=dias
        )

        filtros = ReportService.__gerar_filtros(tipo_medicao, data, data_inicio, data_fim, dias)

        exportador = AnomaliasExport(resultado, tipo_medicao, filtros)
        return exportador.gerar_excel()

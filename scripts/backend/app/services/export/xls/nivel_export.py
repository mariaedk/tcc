"""
@author maria
date: 2025-05-03
"""
from app.schemas.medicao_schema import MedicaoHistoricoSchema
from .excel_base import ExcelExporterBase
from openpyxl.styles import Font

class NivelExport(ExcelExporterBase):
    def __init__(self, dados: list[MedicaoHistoricoSchema], filtros: dict[str, str] = None):
        super().__init__(
            titulo="Evolução do Nível do Tanque (L)",
            subtitulo="Média diária nos últimos dias — variações típicas do sistema.",
            nome_arquivo="nivel_diario",
            filtros=filtros
        )
        self.dados = dados

    def obter_dados(self):
        return [
            {
                "Data": m.data.strftime('%d/%m/%Y'),
                "Valor (L)": m.valor
            }
            for m in self.dados
        ]

    def configurar_colunas_relatorio(self, ws):
        ws.append(["Data", "Valor (L)"])
        ws['A4'].font = ws['B4'].font = Font(bold=True)
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 30

    def configurar_colunas_filtros(self, ws_filtros):
        ws_filtros.column_dimensions['A'].width = 20
        ws_filtros.column_dimensions['B'].width = 20

    def customiza_relatorio(self, ws, dados):
        valores = [dado["Valor (L)"] for dado in dados if "Valor (L)" in dado]
        if valores:
            ws.append([])
            ws.append(["Máximo", max(valores)])
            ws.append(["Mínimo", min(valores)])
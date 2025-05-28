"""
@author maria
date: 2025-05-03
"""
from app.models.enums import TipoMedicao
from app.schemas.medicao_schema import MedicaoHistoricoSchema
from .excel_base import ExcelExporterBase
from openpyxl.styles import Font

class Vazao2Export(ExcelExporterBase):
    def __init__(self, dados: list[MedicaoHistoricoSchema], tipo_medicao: TipoMedicao, filtros: dict[str, str] = None):
        super().__init__(
            titulo="Histórico de Vazão Diária - ETA 2 - (m³/h)",
            subtitulo="Histórico de medições extraídas automaticamente do CLP.",
            nome_arquivo="vazao_eta2",
            filtros=filtros
        )
        self.dados = dados
        self.tipo_medicao = tipo_medicao

    def obter_dados(self):
        return [
            {
                "Data": m.data.strftime('%d/%m/%Y %H:%M') if self.tipo_medicao == TipoMedicao.HORA else m.data.strftime('%d/%m/%Y'),
                "Valor (m³/h)": m.valor
            }
            for m in self.dados
        ]

    def configurar_colunas_relatorio(self, ws):
        ws.append(["Data", "Valor (m³/h)"])
        ws['A4'].font = ws['B4'].font = Font(bold=True)
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 30

    def configurar_colunas_filtros(self, ws_filtros):
        ws_filtros.column_dimensions['A'].width = 20
        ws_filtros.column_dimensions['B'].width = 20

    def customiza_relatorio(self, ws, dados):
        valores = [dado["Valor (m³/h)"] for dado in dados if "Valor (m³/h)" in dado]
        if valores:
            ws.append([])
            ws.append(["Máximo", max(valores)])
            ws.append(["Mínimo", min(valores)])
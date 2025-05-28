"""
@author maria
date: 2025-05-03
"""
from openpyxl.styles import Font

from app.models.enums import TipoMedicao
from app.schemas.medicao_schema import MedicaoHistoricoSchema
from .excel_base import ExcelExporterBase

class VazaoExport(ExcelExporterBase):
    def __init__(self, medicoes: list[MedicaoHistoricoSchema], tipo_medicao: TipoMedicao, filtros: dict[str, str] = None):
        super().__init__(
            titulo="Histórico de Vazão Diária - ETA 1 (m³/h)",
            subtitulo="Histórico de medições extraídas automaticamente do CLP.",
            nome_arquivo="vazao_eta1",
            filtros=filtros
        )
        self.medicoes = medicoes
        self.tipo_medicao = tipo_medicao

    def obter_dados(self):
        return [
            {
                "Data": m.data.strftime('%d/%m/%Y %H:%M') if self.tipo_medicao == TipoMedicao.HORA else m.data.strftime('%d/%m/%Y'),
                "Valor (m³/h)": m.valor
            }
            for m in self.medicoes
        ]

    def configurar_colunas_relatorio(self, ws):
        ws.append(["Data", "Valor (m³/h)"])
        ws['A4'].font = ws['B4'].font = Font(bold=True)
        ws.column_dimensions["A"].width = 30
        ws.column_dimensions["B"].width = 40

    def configurar_colunas_filtros(self, ws_filtros):
        ws_filtros.column_dimensions["A"].width = 20
        ws_filtros.column_dimensions["B"].width = 20

    def customiza_relatorio(self, ws, dados):
        valores = [d["Valor (m³/h)"] for d in dados if isinstance(d.get("Valor (m³/h)"), (int, float))]
        if valores:
            ws.append([])
            ws.append(["Máximo", max(valores)])
            ws.append(["Mínimo", min(valores)])
            ws.append(["Média geral", round(sum(valores) / len(valores), 2)])

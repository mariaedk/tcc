"""
@author maria
date: 2025-05-04
"""
from app.models.enums import TipoMedicao
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import matplotlib.ticker as mticker

class GraficoService:

    @staticmethod
    def gerar_grafico_base64(dados, tipo_medicao: TipoMedicao, titulo_grafico: str, unidade: str = "L"):
        if tipo_medicao == TipoMedicao.DIA:
            datas = [d.data.strftime('%d/%m/%Y') for d in dados]
        else:
            datas = [d.data.strftime('%d/%m/%Y %H:%M') for d in dados]

        valores = [d.valor for d in dados]

        plt.figure(figsize=(10, 5))
        plt.plot(datas, valores, marker='o', linestyle='-', color='green')
        plt.title(titulo_grafico)
        plt.xlabel('Data')
        plt.ylabel(f'Valor ({unidade})')
        plt.grid(True)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=False, prune=None))
        plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.2f}'))
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode('utf-8')
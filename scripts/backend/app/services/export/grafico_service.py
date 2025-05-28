"""
@author maria
date: 2025-05-04
"""
from matplotlib.dates import AutoDateLocator, DateFormatter
import matplotlib.ticker as mticker
from app.models.enums import TipoMedicao
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class GraficoService:

    @staticmethod
    def gerar_grafico_base64(dados, tipo_medicao, titulo_grafico, unidade='m³/h', figsize=(12, 5)):
        if not dados:
            return None

        # Usar datas como datetime puro
        datas = [d.data for d in dados]
        valores = [d.valor for d in dados]

        plt.figure(figsize=figsize)
        plt.plot(datas, valores, linestyle='-', color='green', linewidth=1.1, alpha=0.8)

        plt.title(titulo_grafico)
        plt.xlabel('Data')
        plt.ylabel(f'Valor ({unidade})')
        plt.grid(True, linestyle='--', alpha=0.5)

        ax = plt.gca()

        locator = AutoDateLocator(minticks=8, maxticks=20)

        if tipo_medicao == TipoMedicao.DIA:
            formatter = DateFormatter('%d/%m')
        else:
            formatter = DateFormatter('%d/%m %H:%M')

        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(nbins=15))

        plt.xticks(rotation=45, fontsize=8)
        plt.yticks(fontsize=8)

        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300)
        plt.close()
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode('utf-8')
import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { LineMarkerChart } from 'src/app/models/LineMarkerChart';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
import { AnaliseService } from 'src/app/services/analise/analise.service';
import { ReportService } from 'src/app/services/report/report.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-line-marker-chart',
  templateUrl: './line-marker-chart.component.html',
  styleUrls: ['./line-marker-chart.component.scss']
})
export class LineMarkerChartComponent implements OnInit, OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  chartOptions!: Partial<LineMarkerChart>;
  chartVazio = false;
  unidadeMedida = 'L';

  constructor(private analiseService: AnaliseService, private reportService: ReportService, private snackBar: MatSnackBar) {}

  ngOnInit(): void {

  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados() {
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);
    const dias = this.filtros?.dias;
    const tipoMedicao = this.filtros?.tipoMedicao;

    if ((dataInicio && !dataFim) || (!dataInicio && dataFim)) return;
    if (dataInicio && dataFim && dias) this.filtros.dias = null;

    const formatador: Intl.DateTimeFormatOptions =
      tipoMedicao === TipoMedicao.HORA
        ? { hour: '2-digit', minute: '2-digit' }
        : tipoMedicao === TipoMedicao.DIA
        ? { day: '2-digit', month: '2-digit', year: 'numeric' }
        : { hour: '2-digit', minute: '2-digit' };

    this.analiseService.getAnaliseAutomatica(
      3,
      tipoMedicao,
      dias,
      data,
      dataInicio,
      dataFim
    ).subscribe((res) => {
      const dados = res.dados;
      const categorias = dados.map((d: any) =>
        new Date(d.data).toLocaleString('pt-BR', formatador)
      );
      const valores = dados.map((d: any) => d.valor);
      const anomaliasIndices = dados
        .map((d: any, index: number) => d.is_anomalia ? index : -1)
        .filter((index: number) => index !== -1);
      const unidade = res.unidade ?? 'n/a';
      this.unidadeMedida = unidade;
      this.createChartOptions(anomaliasIndices, valores, categorias, unidade);
    });
  }

  private formatarDataParaApi(data: string | Date | null | undefined): string | undefined {
    if (!data) return undefined;
    const date = new Date(data);
    return isNaN(date.getTime()) ? undefined : date.toISOString();
  }

  createChartOptions(
    anomaliasIndices: number[],
    valores: number[],
    categorias: string[],
    unidade: string
  ) {
    this.chartVazio = valores.length === 0;
    this.chartOptions = {
      series: [
        {
          name: `Nível de água`,
          data: valores
        }
      ],
      chart: {
        type: "line",
        height: 350,
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 800
        },
        locales: [this.localePtBr()],
        defaultLocale: 'pt-br'
      },
      xaxis: {
        categories: categorias,
        type: "category"
      },
      markers: {
        size: 5,
        discrete: anomaliasIndices.map(index => ({
          seriesIndex: 0,
          dataPointIndex: index,
          fillColor: '#FF4560',
          strokeColor: '#fff',
          size: 6
        }))
      },
      stroke: {
        curve: "smooth"
      },
      tooltip: {
        custom: ({ series, seriesIndex, dataPointIndex, w }) => {
          const valor = series[seriesIndex][dataPointIndex];
          const isAnomalia = w.config.markers?.discrete?.some(
            (m: any) => m.dataPointIndex === dataPointIndex
          );

          const label = this.filtros?.tipoMedicao === TipoMedicao.DIA
            ? 'Dia'
            : this.filtros?.tipoMedicao === TipoMedicao.HORA
            ? 'Hora'
            : 'Data/Hora';

          return `
            <div style="padding: 8px;">
              <strong>${isAnomalia ? '⚠ Anomalia detectada<br>' : ''}</strong>
              ${label}: ${w.config.xaxis.categories[dataPointIndex]}<br>
              Nível: ${valor.toFixed(2)} ${unidade}
            </div>
          `;
        }
      },
      yaxis: {
        title: {
          text: `Nível de Água (${unidade})`
        },
        labels: {
          formatter: (val: number) => val.toFixed(2) + ` ${unidade}`
        }
      },
      dataLabels: {
        enabled: false
      }
    };

    setTimeout(() => {
      this.chartLoaded.emit();
    });
  }

  private localePtBr() {
    return {
      name: 'pt-br',
      options: {
        months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        shortMonths: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                      'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        days: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta',
               'Sexta', 'Sábado'],
        shortDays: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
        toolbar: {
          exportToSVG: 'Download SVG',
          exportToPNG: 'Download PNG',
          exportToCSV: 'Download CSV',
          menu: 'Menu',
          selection: 'Selecionar',
          selectionZoom: 'Zoom por Seleção',
          zoomIn: 'Aproximar',
          zoomOut: 'Afastar',
          pan: 'Mover',
          reset: 'Resetar Zoom'
        }
      }
    };
  }

  exportarAnomaliaXls(): void {
    this.reportService.exportarAnomaliaXLS(3, this.filtros?.tipoMedicao, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias)
    .subscribe({
      next: (response) => {
        const contentDisposition = response.headers.get('Content-Disposition');
        const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
        const filename = filenameMatch ? filenameMatch[1] : 'relatorio_anomalia.xlsx';

        saveAs(response.body!, filename);

        this.snackBar.open('XLS baixado com sucesso!', 'Fechar', {
          duration: 3000
        });
      },
      error: (err) => this.snackBar.open('Erro ao baixar XLS.', 'Fechar', { duration: 4000 })
    });
  }

  exportarAnomaliaPdf(): void {
    this.reportService.exportarAnomaliaPDF(3, this.filtros?.tipoMedicao, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias)
    .subscribe({
      next: (response) => {
        const contentDisposition = response.headers.get('Content-Disposition');
        const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
        const filename = filenameMatch ? filenameMatch[1] : 'relatorio_anomalia.pdf';

        saveAs(response.body!, filename);

        this.snackBar.open('PDF baixado com sucesso!', 'Fechar', {
          duration: 3000
        });
      },
      error: (err) => this.snackBar.open('Erro ao baixar PDF.', 'Fechar', { duration: 4000 })
    });
  }
}

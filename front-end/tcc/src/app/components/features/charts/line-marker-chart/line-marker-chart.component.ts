import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { LineMarkerChart } from 'src/app/models/LineMarkerChart';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
import { AnaliseService } from 'src/app/services/analise/analise.service';
import { ReportService } from 'src/app/services/report/report.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DownloadService } from 'src/app/services/download/download.service';

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
  unidadeMedida = '';

  constructor(private analiseService: AnaliseService, private reportService: ReportService, private snackBar: MatSnackBar, private downloadService: DownloadService) {}

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

    if ((dataInicio && !dataFim) || (!dataInicio && dataFim)) {
      this.chartLoaded.emit();
      return;
    }
    if (dataInicio && dataFim && dias) {
      this.filtros.dias = null;
      this.chartLoaded.emit();
      return;
    }

    this.analiseService.getAnaliseAutomatica(2, tipoMedicao, dias, data, dataInicio, dataFim)
      .subscribe((res) => {
        const dados = res.dados;
        const unidade = res.unidade ? res.unidade : 'n/a';
        this.unidadeMedida = unidade;

        const seriesData = dados.map((d: any) => ({
          x: new Date(d.data).getTime(),
          y: d.valor
        }));

        const anomaliasIndices = dados
          .map((d: any, index: number) => d.is_anomalia ? index : -1)
          .filter((index: number) => index !== -1);

        this.createChartOptions(seriesData, anomaliasIndices, tipoMedicao, unidade);
      });
  }

  private formatarDataParaApi(data: string | Date | null | undefined): string | undefined {
    if (!data) return undefined;
    const date = new Date(data);
    return isNaN(date.getTime()) ? undefined : date.toISOString();
  }

  createChartOptions(
    data: { x: number; y: number }[],
    anomaliasIndices: number[],
    tipoMedicao: TipoMedicao,
    unidade: string
  ) {
    this.chartVazio = data.length === 0;
    const unidadeLabel = unidade ? ` (${unidade})` : 'n/a';
    const animacaoAtivada = data.length < 500;

    this.chartOptions = {
      series: [{
        name: 'Vazão da ETA 2',
        data
      }],
      chart: {
        type: 'line',
        height: 350,
        locales: [this.localePtBr()],
        defaultLocale: 'pt-br',
        toolbar: { show: true },
        zoom: { enabled: true },
        animations: {
          enabled: animacaoAtivada,
          easing: 'easeinout',
          speed: 500,
          animateGradually: {
            enabled: animacaoAtivada,
            delay: 150
          },
          dynamicAnimation: {
            enabled: animacaoAtivada,
            speed: 350
          }
        }
      },
      stroke: { curve: 'smooth', width: 3 },
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
      dataLabels: {
        enabled: data.length < 100,
        formatter: (val: number) => `${val.toFixed(2)} ${unidade}`
      },
      xaxis: {
        type: 'datetime',
        labels: {
          formatter: (value: string, timestamp?: number) => {
            const date = new Date(timestamp ?? 0);
            return tipoMedicao === TipoMedicao.DIA
              ? date.toLocaleDateString('pt-BR')
              : `${date.toLocaleDateString('pt-BR')} ${date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}`;
          },
          rotate: -45,
          style: { colors: '#6c757d', fontSize: '12px' }
        },
        title: {
          text: tipoMedicao === TipoMedicao.DIA ? 'Data' : 'Hora',
          style: { color: '#6c757d', fontSize: '14px' }
        }
      },
      yaxis: {
        title: {
          text: `Vazão da ETA 2 ${unidadeLabel}`,
          style: { color: '#6c757d', fontSize: '14px' }
        },
        labels: {
          formatter: (val: number) => `${val.toFixed(2)} ${unidade}`,
          style: { colors: '#6c757d', fontSize: '12px' }
        }
      },
      tooltip: {
        x: {
          formatter: (val: number) => {
            const date = new Date(val);
            return tipoMedicao === TipoMedicao.DIA
              ? `Dia: ${date.toLocaleDateString('pt-BR')}`
              : `${date.toLocaleDateString('pt-BR')} ${date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}`;
          }
        },
        y: {
          formatter: (val: number) => `${val.toFixed(2)} ${unidade}`
        },
        custom: ({ series, seriesIndex, dataPointIndex, w }) => {
          const valor = series[seriesIndex][dataPointIndex];
          const isAnomalia = w.config.markers?.discrete?.some(
            (m: any) => m.dataPointIndex === dataPointIndex
          );

          const label = tipoMedicao === TipoMedicao.DIA ? 'Dia' : 'Hora';
          const dataStr = w.globals.seriesX[seriesIndex][dataPointIndex];
          const dataFormatada = new Date(dataStr).toLocaleString('pt-BR');

          return `
            <div style="padding: 8px;">
              <strong>${isAnomalia ? '⚠ Anomalia detectada<br>' : ''}</strong>
              ${label}: ${dataFormatada}<br>
              Vazão: ${valor.toFixed(2)} ${unidade}
            </div>
          `;
        }
      },
      title: {
        text: 'Análise de Anomalias - Vazão ETA 2',
        align: 'left',
        style: {
          fontSize: '16px',
          color: '#212529'
        }
      }
    };

    setTimeout(() => this.chartLoaded.emit());
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
    if (!this.downloadService.startDownload()) {
      this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 });
      return;
    }
    const snack = this.snackBar.open('Gerando XLS... Por favor aguarde.', undefined, {
      panelClass: 'snackbar-loading'
    });
    this.reportService.exportarAnomaliaXLS(2,
      this.filtros?.tipoMedicao,
      this.formatarDataParaApi(this.filtros?.data),
      this.formatarDataParaApi(this.filtros?.dataInicio),
      this.formatarDataParaApi(this.filtros?.dataFim),
      this.filtros?.dias)
    .subscribe({
      next: (response) => {
        const contentDisposition = response.headers.get('Content-Disposition');
        const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
        const filename = filenameMatch ? filenameMatch[1] : 'relatorio_anomalia.xlsx';

        saveAs(response.body!, filename);

        this.snackBar.open('XLS baixado com sucesso!', 'Fechar', {
          duration: 3000
        });
        this.downloadService.finishDownload();
      },
      error: (err) => {
        this.snackBar.open('Erro ao baixar XLS.', 'Fechar', { duration: 4000 })
        this.downloadService.finishDownload();
      },
      complete: () => snack.dismiss()
    });
  }

  exportarAnomaliaPdf(): void {
    if (!this.downloadService.startDownload()) {
      this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 });
      return;
    }
    const snack = this.snackBar.open('Gerando PDF... Por favor aguarde.', undefined, {
      panelClass: 'snackbar-loading'
    });
    this.reportService.exportarAnomaliaPDF(2,
      this.filtros?.tipoMedicao,
      this.formatarDataParaApi(this.filtros?.data),
      this.formatarDataParaApi(this.filtros?.dataInicio),
      this.formatarDataParaApi(this.filtros?.dataFim),
      this.filtros?.dias)
    .subscribe({
      next: (response) => {
        const contentDisposition = response.headers.get('Content-Disposition');
        const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
        const filename = filenameMatch ? filenameMatch[1] : 'relatorio_anomalia.pdf';

        saveAs(response.body!, filename);

        this.snackBar.open('PDF baixado com sucesso!', 'Fechar', {
          duration: 3000
        });
        this.downloadService.finishDownload();
      },
      error: (err) => {
        this.snackBar.open('Erro ao baixar PDF.', 'Fechar', { duration: 4000 })
        this.downloadService.finishDownload();
      },
      complete: () => snack.dismiss()
    });
  }
}

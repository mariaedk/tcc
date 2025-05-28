import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { LineChartOptions } from 'src/app/models/LineChartOptions';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';
import { ReportService } from 'src/app/services/report/report.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DownloadService } from 'src/app/services/download/download.service';

@Component({
  selector: 'app-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.scss']
})
export class LineChartComponent implements OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  @ViewChild('chart', { static: false }) chart?: ChartComponent;

  chartVazio = false;

  unidadeMedida = "L"

  chartOptions: Partial<LineChartOptions> = {
    series: [],
    chart: { type: 'line', height: 350 },
    xaxis: { categories: [] },
    title: { text: '' }
  };

  constructor(
    private medicaoService: MedicaoService,
    private reportService: ReportService,
    private snackBar: MatSnackBar,
    private downloadService: DownloadService
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros']?.currentValue) {
      this.carregarDados();
    }
  }

  // formata a data para o formato ISO (padrão para FastAPI)
  private formatarDataParaApi(data: string | Date | null | undefined): string | undefined {
    if (!data) return undefined;
    const date = new Date(data);
    return isNaN(date.getTime()) ? undefined : date.toISOString();
  }

  // carrega dados com base no tipo de medição e filtros ativos
  private carregarDados(): void {
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);
    const dias = this.filtros?.dias;

    if (this.filtros?.tipoMedicao === TipoMedicao.HORA && !data) return;
    if (this.filtros?.tipoMedicao === TipoMedicao.DIA && !(dias || (dataInicio && dataFim))) return;

    this.medicaoService.buscarHistorico(1, this.filtros?.tipoMedicao, data, dataInicio, dataFim, dias)
      .subscribe((dados) => {
        const unidade = dados.length > 0 ? dados[0].unidade ?? 'n/a' : 'n/a';
        this.unidadeMedida = unidade;
        const seriesData = dados.map(d => ({
          x: new Date(d.data).getTime(),
          y: d.valor
        }));

        this.createChartOptions(seriesData, this.filtros.tipoMedicao, unidade);
      });
  }

  // monta as configurações do gráfico
  private createChartOptions(
    data: { x: number; y: number }[],
    tipoMedicao: TipoMedicao,
    unidade: string
  ): void {
    this.chartVazio = data.length === 0;

    const unidadeLabel = unidade ? ` (${unidade})` : '';
    const animacaoAtivada = data.length < 500; // ajusta esse limite conforme seu gosto

    this.chartOptions = {
      series: [{ name: 'Medição', data }],
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
      colors: ['#0077b6'],
      stroke: { curve: 'smooth', width: 3 },
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
          text: `Vazão ETA 1 ${unidadeLabel}`,
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
              : `Hora: ${date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}`;
          }
        },
        y: {
          formatter: (val: number) => `${val.toFixed(2)} ${unidade}`
        }
      },
      grid: {
        borderColor: '#e0e0e0',
        strokeDashArray: 4
      }
    };

    setTimeout(() => this.chartLoaded.emit());
  }


  // localização em pt-BR
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

  // exportar XLS
  exportarVazaoXls(): void {
    if (!this.downloadService.startDownload()) {
      this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 });
      return;
    }
    const snack = this.snackBar.open('Gerando XLS... Aguarde.', undefined, {
      panelClass: 'snackbar-loading'
    });
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);

    this.reportService.exportarVazaoXLS(1, this.filtros?.tipoMedicao, data, dataInicio, dataFim, this.filtros?.dias)
      .subscribe({
        next: (response) => {
          this.salvarArquivo(response, 'relatorio_vazao.xlsx');
          this.snackBar.open('XLS baixado com sucesso!', 'Fechar', {
            duration: 3000
          });
        },
        error: (err) => {
          this.snackBar.open('Erro ao baixar XLS.', 'Fechar', { duration: 4000 });
        },
        complete: () => snack.dismiss()
      });
  }

  // exportar PDF
  exportarVazaoPdf(): void {
    if (!this.downloadService.startDownload()) {
      this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 });
      return;
    }
    const snack = this.snackBar.open('Gerando PDF... Aguarde.', undefined, {
      panelClass: 'snackbar-loading'
    });

    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);

    this.reportService.exportarVazaoPDF(1, this.filtros?.tipoMedicao, data, dataInicio, dataFim, this.filtros?.dias)
      .subscribe({
        next: (response) => {
          this.salvarArquivo(response, 'relatorio_vazao.pdf')
          this.snackBar.open('PDF baixado com sucesso!', 'Fechar', {
            duration: 3000
          });
        },
        error: (err) => {
          this.snackBar.open('Erro ao baixar PDF.', 'Fechar', { duration: 4000 });
        },
        complete: () => snack.dismiss()
      });
  }

  // função auxiliar para salvar arquivos
  private salvarArquivo(response: any, fallbackName: string) {
    const contentDisposition = response.headers.get('Content-Disposition');
    const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
    const filename = filenameMatch ? filenameMatch[1] : fallbackName;
    saveAs(response.body!, filename);
  }
}

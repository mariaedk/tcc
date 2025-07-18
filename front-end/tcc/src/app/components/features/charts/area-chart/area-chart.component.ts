import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { AreaChartOptions } from 'src/app/models/AreaChartOptions';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';
import { ReportService } from 'src/app/services/report/report.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { DownloadService } from 'src/app/services/download/download.service';

@Component({
  selector: 'app-area-chart',
  templateUrl: './area-chart.component.html',
  styleUrls: ['./area-chart.component.scss']
})
export class AreaChartComponent implements OnChanges {

  @Input() filtros: any;
  @Input() sensor: any;
  @Output() chartLoaded = new EventEmitter<void>();

  @ViewChild('chartInstance', { static: false }) chart?: ChartComponent;

  chartVazio = false;

  unidadeMedida = "";

  chartOptions: Partial<AreaChartOptions> = {};

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

  // função para formatar datas para API (ISO)
  private formatarDataParaApi(data: string | Date | null | undefined): string | undefined {
    if (!data) return undefined;
    const date = new Date(data);
    return isNaN(date.getTime()) ? undefined : date.toISOString();
  }

  private carregarDados(): void {
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);
    const dias = this.filtros?.dias;

    if (this.filtros?.tipoMedicao === TipoMedicao.HORA && !data){
      this.chartLoaded.emit();
      return;
    }
    if (this.filtros?.tipoMedicao === TipoMedicao.DIA && !(dias || (dataInicio && dataFim))) {
      this.chartLoaded.emit();
      return;
    }

    this.medicaoService.buscarHistorico(this.sensor, this.filtros?.tipoMedicao, data, dataInicio, dataFim, dias)
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


  // configuração do gráfico
  private createChartOptions(
    data: { x: number; y: number }[],
    tipoMedicao: TipoMedicao,
    unidade: string
  ): void {
    this.chartVazio = data.length === 0;

    const unidadeLabel = unidade ? ` (${unidade})` : '';
    const animacaoAtivada = data.length < 500; // Desliga animação se tiver muitos dados

    this.chartOptions = {
      series: [{
        name: 'Medição',
        data
      }],
      chart: {
        type: 'area',
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
      colors: ['#52b788'],
      stroke: {
        curve: 'smooth',
        width: 3
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
          text: `Vazão ETA 2 ${unidadeLabel}`,
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
        }
      },
      title: {
        text: 'Histórico de Nível',
        align: 'left',
        style: {
          fontSize: '16px',
          color: '#212529'
        }
      },
      legend: {
        horizontalAlign: 'left'
      }
    };

    setTimeout(() => this.chartLoaded.emit());
  }

  // localização PT-BR
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

  // exportação XLS
  exportarVazao2(): void {
    if (!this.downloadService.startDownload()) {
      this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 });
      return;
    }
    const snack = this.snackBar.open('Gerando XLS... Por favor aguarde.', undefined, {
      panelClass: 'snackbar-loading'
    });
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);

    this.reportService.exportarVazao2XLS(this.sensor, this.filtros?.tipoMedicao, data, dataInicio, dataFim, this.filtros?.dias)
      .subscribe({
        next: (response) => {
          this.salvarArquivo(response, 'relatorio_vazao_eta2.xlsx')
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

  // exportação PDF
  exportarVazao2PDF(): void {
    if (!this.downloadService.startDownload()) {
      this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 });
      return;
    }
    const snack = this.snackBar.open('Gerando PDF... Por favor aguarde.', undefined, {
      panelClass: 'snackbar-loading'
    });
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);

    this.reportService.exportarVazao2PDF(this.sensor, this.filtros?.tipoMedicao, data, dataInicio, dataFim, this.filtros?.dias)
      .subscribe({
        next: (response) => {
          this.salvarArquivo(response, 'relatorio_vazao_eta2.pdf')
          this.snackBar.open('PDF baixado com sucesso!', 'Fechar', {
            duration: 3000
          });
          this.downloadService.finishDownload();
        },
        error: (err) => {
          this.snackBar.open('Erro ao baixar PDF.', 'Fechar', { duration: 4000 });
          this.downloadService.finishDownload();
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

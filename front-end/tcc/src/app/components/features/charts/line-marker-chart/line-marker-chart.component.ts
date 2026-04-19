import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import type { EChartsOption } from 'echarts';
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
export class LineMarkerChartComponent implements OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  chartVazio = false;
  unidadeMedida = '';
  chartOption: EChartsOption = {};

  constructor(
    private analiseService: AnaliseService,
    private reportService: ReportService,
    private snackBar: MatSnackBar,
    private downloadService: DownloadService
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros']?.currentValue) {
      this.carregarDados();
    }
  }

  private formatarDataParaApi(data: string | Date | null | undefined): string | undefined {
    if (!data) return undefined;
    const date = new Date(data);
    return isNaN(date.getTime()) ? undefined : date.toISOString();
  }

  carregarDados(): void {
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);
    const dias = this.filtros?.dias;
    const tipoMedicao = this.filtros?.tipoMedicao;

    if ((dataInicio && !dataFim) || (!dataInicio && dataFim)) { this.chartLoaded.emit(); return; }
    if (dataInicio && dataFim && dias) { this.filtros.dias = null; this.chartLoaded.emit(); return; }

    this.analiseService.getAnaliseAutomatica(2, tipoMedicao, dias, data, dataInicio, dataFim)
      .subscribe((res) => {
        const dados = res.dados;
        const unidade = res.unidade ?? 'n/a';
        this.unidadeMedida = unidade;
        this.chartVazio = dados.length === 0;

        const normais: [number, number][] = [];
        const anomalias: [number, number][] = [];

        dados.forEach((d: any) => {
          const ponto: [number, number] = [new Date(d.data).getTime(), d.valor];
          if (d.is_anomalia) anomalias.push(ponto);
          else normais.push(ponto);
        });

        const todosDados: [number, number][] = dados.map((d: any) => [new Date(d.data).getTime(), d.valor]);
        this.chartOption = this.buildOption(todosDados, anomalias, unidade, tipoMedicao);
        setTimeout(() => this.chartLoaded.emit());
      });
  }

  private buildOption(
    todos: [number, number][],
    anomalias: [number, number][],
    unidade: string,
    tipoMedicao: TipoMedicao
  ): EChartsOption {
    const isDia = tipoMedicao === TipoMedicao.DIA;
    return {
      title: { text: 'Análise de Anomalias - Vazão ETA 2', left: 0, textStyle: { fontSize: 16, color: '#212529' } },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          const p = params[0];
          const d = new Date(p.value[0]);
          const dataStr = isDia ? d.toLocaleDateString('pt-BR') : d.toLocaleString('pt-BR');
          const anomaliaSet = new Set(anomalias.map(a => a[0]));
          const isAnomalia = anomaliaSet.has(p.value[0]);
          return `${isAnomalia ? '<b>⚠ Anomalia detectada</b><br/>' : ''}${dataStr}<br/>${p.value[1].toFixed(2)} ${unidade}`;
        }
      },
      xAxis: {
        type: 'time',
        axisLabel: {
          formatter: (val: number) => {
            const d = new Date(val);
            return isDia ? d.toLocaleDateString('pt-BR') : d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
          },
          rotate: 45,
          color: '#6c757d'
        },
        name: isDia ? 'Data' : 'Hora',
        nameLocation: 'middle',
        nameGap: 40
      },
      yAxis: {
        type: 'value',
        name: `Vazão ETA 2 (${unidade})`,
        nameLocation: 'middle',
        nameGap: 50,
        axisLabel: { formatter: (v: number) => `${v.toFixed(2)}`, color: '#6c757d' }
      },
      dataZoom: [{ type: 'inside' }, { type: 'slider', height: 20 }],
      series: [
        {
          type: 'line',
          data: todos,
          smooth: true,
          lineStyle: { color: '#0077b6', width: 2 },
          itemStyle: { color: '#0077b6' },
          showSymbol: todos.length < 200,
          symbolSize: 4
        },
        {
          type: 'scatter',
          data: anomalias,
          symbolSize: 10,
          itemStyle: { color: '#FF4560' },
          z: 10
        }
      ],
      grid: { left: 70, right: 20, top: 50, bottom: 70 }
    };
  }

  exportarAnomaliaXls(): void {
    if (!this.downloadService.startDownload()) { this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 }); return; }
    const snack = this.snackBar.open('Gerando XLS... Por favor aguarde.', undefined, { panelClass: 'snackbar-loading' });
    this.reportService.exportarAnomaliaXLS(2, this.filtros?.tipoMedicao,
      this.formatarDataParaApi(this.filtros?.data),
      this.formatarDataParaApi(this.filtros?.dataInicio),
      this.formatarDataParaApi(this.filtros?.dataFim),
      this.filtros?.dias)
      .subscribe({
        next: (response) => {
          const contentDisposition = response.headers.get('Content-Disposition');
          const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
          saveAs(response.body!, filenameMatch ? filenameMatch[1] : 'relatorio_anomalia.xlsx');
          this.snackBar.open('XLS baixado com sucesso!', 'Fechar', { duration: 3000 });
          this.downloadService.finishDownload();
        },
        error: () => { this.snackBar.open('Erro ao baixar XLS.', 'Fechar', { duration: 4000 }); this.downloadService.finishDownload(); },
        complete: () => snack.dismiss()
      });
  }
}

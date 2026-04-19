import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import type { EChartsOption } from 'echarts';
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
  @Input() sensor: any;
  @Output() chartLoaded = new EventEmitter<void>();

  chartVazio = false;
  unidadeMedida = 'L';
  chartOption: EChartsOption = {};

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

    if (this.filtros?.tipoMedicao === TipoMedicao.HORA && !data) { this.chartLoaded.emit(); return; }
    if (this.filtros?.tipoMedicao === TipoMedicao.DIA && !(dias || (dataInicio && dataFim))) { this.chartLoaded.emit(); return; }
    if (this.filtros?.tipoMedicao === TipoMedicao.INST && !(dataInicio && dataFim)) { this.chartLoaded.emit(); return; }

    this.medicaoService.buscarHistorico(this.sensor, this.filtros?.tipoMedicao, data, dataInicio, dataFim, dias)
      .subscribe({
        next: (dados: any[]) => {
          const unidade = dados.length > 0 ? dados[0].unidade ?? 'n/a' : 'n/a';
          this.unidadeMedida = unidade;
          this.chartVazio = dados.length === 0;
          const seriesData: [number, number][] = dados.map((d: any) => [new Date(d.data).getTime(), d.valor]);
          this.chartOption = this.buildOption(seriesData, unidade, this.filtros.tipoMedicao);
          setTimeout(() => this.chartLoaded.emit());
        },
        error: () => { this.chartVazio = true; this.chartLoaded.emit(); }
      });
  }

  private buildOption(data: [number, number][], unidade: string, tipoMedicao: TipoMedicao): EChartsOption {
    const isDia = tipoMedicao === TipoMedicao.DIA;
    return {
      title: { text: 'Histórico de Nível - ETA 1', left: 0, textStyle: { fontSize: 16, color: '#212529' } },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => {
          const p = params[0];
          const d = new Date(p.value[0]);
          const dataStr = isDia ? d.toLocaleDateString('pt-BR') : d.toLocaleString('pt-BR');
          return `${dataStr}<br/>${p.value[1].toFixed(2)} ${unidade}`;
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
        name: `Vazão ETA 1 (${unidade})`,
        nameLocation: 'middle',
        nameGap: 50,
        axisLabel: { formatter: (v: number) => `${v.toFixed(2)}`, color: '#6c757d' }
      },
      dataZoom: [{ type: 'inside' }, { type: 'slider', height: 20 }],
      series: [({
        type: 'line',
        data,
        smooth: data.length < 500,
        large: true,
        largeThreshold: 1000,
        sampling: 'lttb',
        lineStyle: { color: '#0077b6', width: 2 },
        itemStyle: { color: '#0077b6' },
        showSymbol: data.length < 200,
        symbolSize: 4
      }) as any],
      grid: { left: 70, right: 20, top: 50, bottom: 70 }
    };
  }

  exportarVazaoXls(): void {
    if (!this.downloadService.startDownload()) { this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 }); return; }
    const snack = this.snackBar.open('Gerando XLS... Por favor aguarde.', undefined, { panelClass: 'snackbar-loading' });
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);
    this.reportService.exportarVazaoXLS(this.sensor, this.filtros?.tipoMedicao, data, dataInicio, dataFim, this.filtros?.dias)
      .subscribe({
        next: (response) => { this.salvarArquivo(response, 'relatorio_vazao_eta1.xlsx'); this.snackBar.open('XLS baixado com sucesso!', 'Fechar', { duration: 3000 }); this.downloadService.finishDownload(); },
        error: () => { this.snackBar.open('Erro ao baixar XLS.', 'Fechar', { duration: 4000 }); this.downloadService.finishDownload(); },
        complete: () => snack.dismiss()
      });
  }

  exportarVazaoPdf(): void {
    if (!this.downloadService.startDownload()) { this.snackBar.open('Aguarde... já existe um download em andamento.', 'Fechar', { duration: 3000 }); return; }
    const snack = this.snackBar.open('Gerando PDF... Por favor aguarde.', undefined, { panelClass: 'snackbar-loading' });
    const data = this.formatarDataParaApi(this.filtros?.data);
    const dataInicio = this.formatarDataParaApi(this.filtros?.dataInicio);
    const dataFim = this.formatarDataParaApi(this.filtros?.dataFim);
    this.reportService.exportarVazaoPDF(this.sensor, this.filtros?.tipoMedicao, data, dataInicio, dataFim, this.filtros?.dias)
      .subscribe({
        next: (response) => { this.salvarArquivo(response, 'relatorio_vazao_eta1.pdf'); this.snackBar.open('PDF baixado com sucesso!', 'Fechar', { duration: 3000 }); this.downloadService.finishDownload(); },
        error: () => { this.snackBar.open('Erro ao baixar PDF.', 'Fechar', { duration: 4000 }); this.downloadService.finishDownload(); },
        complete: () => snack.dismiss()
      });
  }

  private salvarArquivo(response: any, fallbackName: string) {
    const contentDisposition = response.headers.get('Content-Disposition');
    const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
    saveAs(response.body!, filenameMatch ? filenameMatch[1] : fallbackName);
  }
}

import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { LineMarkerChart } from 'src/app/models/LineMarkerChart';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
import { AnaliseService } from 'src/app/services/analise/analise.service';
import { ReportService } from 'src/app/services/report/report.service';

@Component({
  selector: 'app-line-marker-chart',
  templateUrl: './line-marker-chart.component.html',
  styleUrls: ['./line-marker-chart.component.scss']
})
export class LineMarkerChartComponent implements OnInit, OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  chartOptions!: Partial<LineMarkerChart>;

  constructor(private analiseService: AnaliseService, private reportService: ReportService) {}

  ngOnInit(): void {

  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados() {
    const { data, dataInicio, dataFim, dias, tipoMedicao } = this.filtros;

    if ((dataInicio && !dataFim) || (!dataInicio && dataFim)) return;

    const formatador: Intl.DateTimeFormatOptions =
      tipoMedicao === TipoMedicao.HORA
      ? { hour: '2-digit', minute: '2-digit' }
      : { day: '2-digit', month: '2-digit', year: 'numeric' };


    if (tipoMedicao === TipoMedicao.HORA) {
      this.analiseService.getAnaliseAutomaticaHora(3, data).subscribe((res) => {
        const dados = res.dados;
        const categorias = dados.map((d: any) =>
          new Date(d.data).toLocaleString('pt-BR', formatador)
        );
        const valores = dados.map((d: any) => d.valor);
        const anomaliasIndices = dados
          .map((d: any, index: number) => d.is_anomalia ? index : -1)
          .filter((index: number) => index !== -1);

        this.createChartOptions(anomaliasIndices, valores, categorias);
      });
    }

    if (tipoMedicao === TipoMedicao.DIA) {
      this.analiseService.getAnaliseAutomaticaGeral(3, dias, data, dataInicio, dataFim).subscribe((res) => {
        const dados = res.dados;
        const categorias = dados.map((d: any) =>
          new Date(d.data).toLocaleString('pt-BR', formatador)
        );
        const valores = dados.map((d: any) => d.valor);
        const anomaliasIndices = dados
          .map((d: any, index: number) => d.is_anomalia ? index : -1)
          .filter((index: number) => index !== -1);

        this.createChartOptions(anomaliasIndices, valores, categorias);
      });
    }
  }

  createChartOptions(anomaliasIndices: number[], valores: number[], categorias: string[]) {
    this.chartOptions = {
      series: [
        {
          name: "Nível de água",
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
        locales: [{
          name: 'pt-br',
          options: {
            months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
            shortMonths: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            days: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
            shortDays: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab'],
            toolbar: {
              exportToSVG: 'Baixar SVG',
              exportToPNG: 'Baixar PNG',
              exportToCSV: 'Baixar CSV',
              menu: 'Menu',
              selection: 'Selecionar',
              selectionZoom: 'Zoom por seleção',
              zoomIn: 'Aproximar',
              zoomOut: 'Afastar',
              pan: 'Mover',
              reset: 'Resetar zoom',
            }
          }
        }],
        defaultLocale: 'pt-br'
      },
      xaxis: {
        categories: categorias,
        type: "category",
        labels: {
          datetimeFormatter: {
            day: "dd/MM/yyyy",
            month: "MM/yyyy",
            year: "yyyy"
          }
        }
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

          return `
            <div style="padding: 8px;">
              <strong>${isAnomalia ? '⚠ Anomalia detectada<br>' : ''}</strong>
              Nível: ${valor.toFixed(2)} L
            </div>
          `;
        }
      },
      yaxis: {
        title: {
          text: "Nível de Água (L)"
        },
        labels: {
          formatter: (val: number) => val.toFixed(2)
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

  exportarAnomaliaXls(): void {
    this.reportService.exportarAnomaliaXLS(3, this.filtros?.tipoMedicao, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias)
    .subscribe({
      next: (response) => {
        const contentDisposition = response.headers.get('Content-Disposition');
        const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
        const filename = filenameMatch ? filenameMatch[1] : 'relatorio_anomalia.xlsx';

        saveAs(response.body!, filename);
      },
      error: (err) => console.error('Erro ao exportar:', err)
    });
  }
}

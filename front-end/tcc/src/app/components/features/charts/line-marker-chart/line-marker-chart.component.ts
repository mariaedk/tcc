import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { DadoAnalise } from 'src/app/models/DadoAnalise';
import { LineMarkerChart } from 'src/app/models/LineMarkerChart';
import { AnaliseService } from 'src/app/services/analise/analise.service';

@Component({
  selector: 'app-line-marker-chart',
  templateUrl: './line-marker-chart.component.html',
  styleUrls: ['./line-marker-chart.component.scss']
})
export class LineMarkerChartComponent implements OnInit, OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  chartOptions!: Partial<LineMarkerChart>;

  constructor(private analiseService: AnaliseService) {}

  ngOnInit(): void {

  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados() {
    const { data, dataInicio, dataFim, dias } = this.filtros;

    if ((dataInicio && !dataFim) || (!dataInicio && dataFim)) {
      return;
    }

    this.analiseService.getAnaliseAutomatica(3, dias, data, dataInicio, dataFim).subscribe((res) => {
      const categorias = res.dados.map((d: any) => new Date(d.data).toLocaleDateString());
      const valores = res.dados.map((d: any) => d.valor);
      const anomaliasIndices: number[] = (res.dados as DadoAnalise[])
      .map((d, index) => d.is_anomalia ? index : -1)
      .filter((index) => index !== -1);

      this.createChartOptions(anomaliasIndices, valores, categorias);
    });
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
        type: "datetime",
        labels: {
          format: "dd/MM/yyyy",
          datetimeUTC: false,
          datetimeFormatter: {
            day: "dd MMM",
            month: "MMM yyyy",
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
}

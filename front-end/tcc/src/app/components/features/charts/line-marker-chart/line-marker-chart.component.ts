import { Component, EventEmitter, Output } from '@angular/core';
import { ChartOptions } from 'chart.js';
import { LineMarkerChart } from 'src/app/models/LineMarkerChart';
import { AnaliseService } from 'src/app/services/analise/analise.service';

@Component({
  selector: 'app-line-marker-chart',
  templateUrl: './line-marker-chart.component.html',
  styleUrls: ['./line-marker-chart.component.scss']
})
export class LineMarkerChartComponent {

  @Output() chartLoaded = new EventEmitter<void>();

  chartOptions!: Partial<LineMarkerChart>;

  constructor(private analiseService: AnaliseService) {

  }

  ngOnInit(): void {
    this.analiseService.getAnaliseAutomatica(3, 20).subscribe(res => {
      const categorias: string[] = res.dados.map((d: any) => new Date(d.data).toLocaleDateString());
      const valores: number[] = res.dados.map((d: any) => d.valor);
      const anomaliasIndices: number[] = res.dados
        .map((d: any, index: number) => d.is_anomalia ? index : -1)
        .filter((index: number) => index !== -1);

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
          locales: [{
            name: 'pt-br',
            options: {
              months: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
              shortMonths: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
              days: ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'],
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
                reset: 'Resetar Zoom',
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
          y: {
            formatter: function (val: number) {
              return val.toFixed(2);
            }
          }
        },
        yaxis: {
          title: {
            text: "Vazão Média (L/s)"
          },
          labels: {
            formatter: function (val: number) {
              return val.toFixed(2); // exibe só 2 casas decimais
            }
          }
        },
        dataLabels: {
          enabled: false
        },
        title: {
          text: "Nível de água - Análise com Anomalias",
          align: "left"
        }
      };

      this.chartLoaded.emit();
    });
  }

}

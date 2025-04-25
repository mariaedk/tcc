import { Component, EventEmitter, Output, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { LineChartOptions } from 'src/app/models/LineChartOptions';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';

@Component({
  selector: 'app-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.scss']
})
export class LineChartComponent {

  @Output() chartLoaded = new EventEmitter<void>();

  @ViewChild("chart", { static: false }) chart?: ChartComponent;
  chartOptions: Partial<LineChartOptions> = {
    series: [],
    chart: { type: 'line', height: 350 },
    xaxis: { categories: [] },
    title: { text: '' }
  };

  constructor(private medicaoService: MedicaoService) {
    this.chartOptions = {};
  }

  ngOnInit(): void {
    this.medicaoService.getHistoricoSensor(1, 20).subscribe((dados) => {
      const categorias: string[] = dados.map(d => new Date(d.data).toLocaleDateString());
      const valores: number[] = dados.map(d => d.valor);

      this.chartOptions = {
        series: [
          {
            name: "Média Diária Sensor Vazão",
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
        colors: ['#0077b6'],
        title: {
          text: "Histórico de Vazão - Sensor 1"
        },
        xaxis: {
          categories: categorias,
          type: "datetime",
          labels: {
            datetimeFormatter: {
              year: "yyyy",
              month: "MM/yyyy",
              day: "dd/MM",
            }
          }
        },
        stroke: {
          curve: "smooth"
        },
        dataLabels: {
          enabled: true
        }
      };

      setTimeout(() => {
        this.chartLoaded.emit();
      });
    });
  }
}

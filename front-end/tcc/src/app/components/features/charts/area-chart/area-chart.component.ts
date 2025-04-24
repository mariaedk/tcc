import { Component, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { AreaChartOptions } from 'src/app/models/AreaChartOptions';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';

@Component({
  selector: 'app-area-chart',
  templateUrl: './area-chart.component.html',
  styleUrls: ['./area-chart.component.scss']
})
export class AreaChartComponent {

  @ViewChild("chart", { static: false }) chart?: ChartComponent;
  chartOptions: Partial<AreaChartOptions> = {
    series: [],
    chart: { type: 'line', height: 350 },
    xaxis: { categories: [] },
    title: { text: '' }
  };

  constructor(private medicaoService: MedicaoService) {
    this.chartOptions = {};
  }

  ngOnInit(): void {
    this.medicaoService.getHistoricoSensor(3, 20).subscribe((dados) => {
      const categorias: string[] = dados.map(d => new Date(d.data).toLocaleDateString());
      const valores: number[] = dados.map(d => d.valor);

      this.chartOptions = {
        series: [
          {
            name: "Nível do tanque",
            data: valores
          }
        ],
        chart: {
          type: "area",
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
          defaultLocale: 'pt-br',
          zoom: {
            enabled: true
          }
        },
        dataLabels: {
          enabled: true
        },
        stroke: {
          curve: "straight"
        },

        title: {
          text: "Histórico do Nível do Tanque - Sensor 3",
          align: "left"
        },
        labels: categorias,
        xaxis: {
          type: "datetime"
        },
        yaxis: {
          opposite: true
        },
        legend: {
          horizontalAlign: "left"
        }
      };

    });
  }

}

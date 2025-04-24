import { Component, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { VerticalBarChartOptions } from 'src/app/models/VerticalBarChartOptions';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';

@Component({
  selector: 'app-vertical-bar-chart',
  templateUrl: './vertical-bar-chart.component.html',
  styleUrls: ['./vertical-bar-chart.component.scss']
})
export class VerticalBarChartComponent {

  @ViewChild("chart", { static: false }) chart?: ChartComponent;
  chartOptions: Partial<VerticalBarChartOptions> = {
    series: [],
    chart: { type: 'line', height: 350 },
    xaxis: { categories: [] }
  };

  constructor(private medicaoService: MedicaoService) {
    this.chartOptions = {};
  }

  ngOnInit(): void {

    this.medicaoService.getCompararVazoesPorDia(1, 2, 20).subscribe((schema) => {
      this.chartOptions = {
        series: schema.series.map(serie => ({
          name: serie.name,
          data: serie.data
        })),
        chart: {
          type: "bar",
          height: 350
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "55%"
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          show: true,
          width: 2,
          colors: ["transparent"]
        },
        xaxis: {
          categories: schema.categorias
        },
        yaxis: {
          title: {
            text: "Vazão média"
          }
        },
        fill: {
          opacity: 1
        },
        tooltip: {
          y: {
            formatter: function(val: number) {
              return val.toFixed(2) + " m³/s";
            }
          }
        }
      };
    });
  }

}

import { Component, EventEmitter, Output, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { VerticalBarChartOptions } from 'src/app/models/VerticalBarChartOptions';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';

@Component({
  selector: 'app-vertical-bar-chart',
  templateUrl: './vertical-bar-chart.component.html',
  styleUrls: ['./vertical-bar-chart.component.scss']
})
export class VerticalBarChartComponent {

  @Output() chartLoaded = new EventEmitter<void>();

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

    this.medicaoService.getCompararVazoesPorMes(1, 2, 6).subscribe((schema) => {
      this.chartOptions = {
        series: schema.series,
        chart: {
          type: "bar",
          height: 350,
          toolbar: {
            show: true
          },
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: "55%",
          }
        },
        colors: ['#0077b6', '#43aa8b'],
        dataLabels: {
          enabled: false
        },
        stroke: {
          show: true,
          width: 2,
          colors: ["transparent"]
        },
        xaxis: {
          categories: schema.categorias,
          labels: {
            formatter: function (val: string) {
              const [mesAbrev, ano] = val.split('/');
              const mapaMeses: { [key: string]: string } = {
                Jan: 'Janeiro',
                Feb: 'Fevereiro',
                Mar: 'Março',
                Apr: 'Abril',
                May: 'Maio',
                Jun: 'Junho',
                Jul: 'Julho',
                Aug: 'Agosto',
                Sep: 'Setembro',
                Oct: 'Outubro',
                Nov: 'Novembro',
                Dec: 'Dezembro'
              };

              return `${mapaMeses[mesAbrev] || mesAbrev}/${ano}`;
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
        fill: {
          opacity: 1
        },

      };

      setTimeout(() => {
        this.chartLoaded.emit();
      });
    });

  }

}

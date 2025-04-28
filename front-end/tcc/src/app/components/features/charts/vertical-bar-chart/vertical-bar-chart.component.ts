import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { ComparativoVazaoResponseSchema } from 'src/app/models/ComparativoVazaoResponseSchema';
import { DadoAnalise } from 'src/app/models/DadoAnalise';
import { VerticalBarChartOptions } from 'src/app/models/VerticalBarChartOptions';
import { AnaliseService } from 'src/app/services/analise/analise.service';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';

@Component({
  selector: 'app-vertical-bar-chart',
  templateUrl: './vertical-bar-chart.component.html',
  styleUrls: ['./vertical-bar-chart.component.scss']
})
export class VerticalBarChartComponent implements OnChanges, OnInit {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  @ViewChild("chart", { static: false }) chart?: ChartComponent;
  chartOptions: Partial<VerticalBarChartOptions> = {
    series: [],
    chart: { type: 'line', height: 350 },
    xaxis: { categories: [] }
  };

  constructor(private medicaoService: MedicaoService) {}

  ngOnInit(): void {
    this.carregarDados();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados() {
    const { dataInicio, dataFim } = this.filtros;

    if ((dataInicio && !dataFim) || (!dataInicio && dataFim)) {
      return;
    }

    this.medicaoService.getCompararVazoesPorMes(1, 2, 6, dataInicio, dataFim).subscribe((res) => {
      this.createChartOptions(res);
    });
  }

  createChartOptions(res : ComparativoVazaoResponseSchema) {
    this.chartOptions = {
      series: res.series,
      chart: {
        type: "bar",
        height: 350,
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 800
        },
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
        categories: res.categorias,
        labels: {
          formatter: function (val: string) {
            const [ano, mesNumero] = val.split('-');
            const mapaMeses: { [key: string]: string } = {
              '01': 'Janeiro',
              '02': 'Fevereiro',
              '03': 'Março',
              '04': 'Abril',
              '05': 'Maio',
              '06': 'Junho',
              '07': 'Julho',
              '08': 'Agosto',
              '09': 'Setembro',
              '10': 'Outubro',
              '11': 'Novembro',
              '12': 'Dezembro'
            };

            return `${mapaMeses[mesNumero] || mesNumero}/${ano}`;
          }
        }
      },
      yaxis: {
        title: {
          text: "Vazão Média (L/s)"
        },
        labels: {
          formatter: function (val: number) {
            return val.toFixed(2);
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
  }

}

import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { AreaChartOptions } from 'src/app/models/AreaChartOptions';
import { TipoConsulta } from 'src/app/models/TIpoConsulta';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';

@Component({
  selector: 'app-area-chart',
  templateUrl: './area-chart.component.html',
  styleUrls: ['./area-chart.component.scss']
})
export class AreaChartComponent implements OnInit, OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  dias = 20;

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

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  ngOnInit(): void {
    this.carregarDados();
  }

  carregarDados() {
    if (this.filtros?.tipoConsulta == TipoConsulta.MEDIA) {
      this.medicaoService.buscarMediaPorDia(3, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias).subscribe((dados) => {
        const categorias: string[] = dados.map(d => new Date(d.data).toLocaleDateString());
        const valores: number[] = dados.map(d => d.valor);
        this.createChartOptions(valores, categorias)
      });
    }

    if (this.filtros?.tipoConsulta == TipoConsulta.GERAL) {
      this.medicaoService.buscarMediaPorDia(3, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias).subscribe((dados) => {
        const categorias: string[] = dados.map(d => new Date(d.data).toLocaleDateString());
        const valores: number[] = dados.map(d => d.valor);
        this.createChartOptions(valores, categorias)
      });
    }
  }

  createChartOptions(valores: number[], categorias: string[]) {
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
      colors: ['#52b788'],
      dataLabels: {
        enabled: true
      },
      stroke: {
        curve: "straight"
      },
      labels: categorias,
      xaxis: {
        type: "datetime",
        labels: { style: { colors: '#343a40' } }
      },
      yaxis: {
        opposite: true,
        labels: { style: { colors: '#343a40' } }
      },
      legend: {
        horizontalAlign: "left"
      }
    };

    setTimeout(() => {
      this.chartLoaded.emit();
    });
  }

}

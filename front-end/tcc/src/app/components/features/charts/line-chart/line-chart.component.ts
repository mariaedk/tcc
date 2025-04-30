import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { LineChartOptions } from 'src/app/models/LineChartOptions';
import { TipoConsulta } from 'src/app/models/TipoConsulta';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';

@Component({
  selector: 'app-line-chart',
  templateUrl: './line-chart.component.html',
  styleUrls: ['./line-chart.component.scss']
})
export class LineChartComponent implements OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  initialized = false;

  @ViewChild("chart", { static: false }) chart?: ChartComponent;
  chartOptions: Partial<LineChartOptions> = {
    series: [],
    chart: { type: 'line', height: 350 },
    xaxis: { categories: [] },
    title: { text: '' }
  };

  constructor(private medicaoService: MedicaoService) {

  }

  ngOnInit() {
    this.initialized = true;
    this.buscarDados();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!this.initialized) {
      return;
    }

    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados() {
    if (TipoConsulta.MEDIA == this.filtros.tipoConsulta && ((this.filtros.dataInicio && !this.filtros.dataFim) || (!this.filtros.dataInicio && this.filtros.dataFim)
      || (!this.filtros.dataInicio && !this.filtros.dataFim && !this.filtros.dias))) {
      return;
    }

    if (TipoConsulta.HORA == this.filtros.tipoConsulta && (!this.filtros.data)) {
      return;
    }

    this.buscarDados();
  }

  buscarDados() {
    if (this.filtros?.tipoConsulta == TipoConsulta.MEDIA) {
      this.medicaoService.buscarMediaPorDia(1, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias).subscribe((dados) => {
        const seriesData = dados.map(d => ({
          x: new Date(d.data),
          y: d.valor
        }));
        this.createChartOptions(seriesData)
      });
    }

    if (this.filtros?.tipoConsulta == TipoConsulta.HORA) {
      this.medicaoService.buscarPorHora(1, this.filtros?.data).subscribe((dados) => {
        const seriesData = dados.map(d => ({
          x: new Date(d.data),
          y: d.valor
        }));
        this.createChartOptions(seriesData)
      });
    }
  }

  createChartOptions(data: { x: Date; y: number }[]): void {
    this.chartOptions = {
      series: [
        {
          name: "Média Diária Sensor Vazão",
          data: data
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
      xaxis: {
        categories: data,
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
  }
}

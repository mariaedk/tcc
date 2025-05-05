import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { LineChartOptions } from 'src/app/models/LineChartOptions';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';
import { ReportService } from 'src/app/services/report/report.service';

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

  constructor(private medicaoService: MedicaoService, private reportService: ReportService) {

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
    if (TipoMedicao.DIA == this.filtros.tipoMedicao && ((this.filtros.dataInicio && !this.filtros.dataFim) || (!this.filtros.dataInicio && this.filtros.dataFim)
      || (!this.filtros.dataInicio && !this.filtros.dataFim && !this.filtros.dias))) {
      return;
    }

    if (TipoMedicao.HORA == this.filtros.tipoMedicao && (!this.filtros.data)) {
      return;
    }

    this.buscarDados();
  }

  buscarDados() {
    if (this.filtros?.tipoMedicao == TipoMedicao.DIA) {
      this.medicaoService.buscarMediaPorDia(1, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias).subscribe((dados) => {
        const seriesData = dados.map(d => ({
          x: new Date(d.data),
          y: d.valor
        }));
        this.createChartOptions(seriesData)
      });
    }

    if (this.filtros?.tipoMedicao == TipoMedicao.HORA) {
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
            day: "dd/MM/yyyy",
            month: "MM/yyyy",
            year: "yyyy"
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

    exportarVazaoXls(): void {
      this.reportService.exportarVazaoXLS(1, this.filtros?.tipoMedicao, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias)
      .subscribe({
        next: (response) => {
          const contentDisposition = response.headers.get('Content-Disposition');
          const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
          const filename = filenameMatch ? filenameMatch[1] : 'relatorio_vazao.xlsx';

          saveAs(response.body!, filename);
        },
        error: (err) => console.error('Erro ao exportar:', err)
      });
    }

    exportarVazaoPdf(): void {
      this.reportService.exportarVazaoPDF(1, this.filtros?.tipoMedicao, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias)
      .subscribe({
        next: (response) => {
          const contentDisposition = response.headers.get('Content-Disposition');
          const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
          const filename = filenameMatch ? filenameMatch[1] : 'relatorio_vazao.xlsx';

          saveAs(response.body!, filename);
        },
        error: (err) => console.error('Erro ao exportar:', err)
      });
    }
}

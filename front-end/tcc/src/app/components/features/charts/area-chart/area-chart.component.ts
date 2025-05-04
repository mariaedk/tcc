import { saveAs } from 'file-saver';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { ChartComponent } from 'ng-apexcharts';
import { AreaChartOptions } from 'src/app/models/AreaChartOptions';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';
import { ReportService } from 'src/app/services/report/report.service';

@Component({
  selector: 'app-area-chart',
  templateUrl: './area-chart.component.html',
  styleUrls: ['./area-chart.component.scss']
})
export class AreaChartComponent implements OnChanges {

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

  constructor(private medicaoService: MedicaoService, private reportService: ReportService) {
    this.chartOptions = {};
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados() {
    const { tipoMedicao, data, dataInicio, dataFim, dias } = this.filtros;

    if (
      (tipoMedicao === TipoMedicao.DIA &&
        ((dataInicio && !dataFim) || (!dataInicio && dataFim) || (!dataInicio && !dataFim && !dias))) ||
      (tipoMedicao === TipoMedicao.HORA && !data)
    ) {
      return;
    }

    if (this.filtros?.tipoMedicao == TipoMedicao.DIA) {
      this.medicaoService.buscarMediaPorDia(3, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias)
        .subscribe((dados) => {
          const categorias: string[] = dados.map(d =>
            new Date(d.data).toLocaleDateString('pt-BR')
          );
          const valores: number[] = dados.map(d => d.valor);
          this.createChartOptions(valores, categorias);
        });
    }

    if (tipoMedicao === TipoMedicao.HORA) {
      this.medicaoService.buscarPorHora(3, data).subscribe((dados) => {
        const todosMesmoDia = dados.every((d: any) =>
          new Date(d.data).toDateString() === new Date(dados[0].data).toDateString()
        );

        const formatadorHora: Intl.DateTimeFormatOptions = todosMesmoDia
          ? { hour: '2-digit', minute: '2-digit' }
          : { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit' };

        const categorias = dados.map((d: any) =>
          new Date(d.data).toLocaleString('pt-BR', formatadorHora)
        );
        const valores = dados.map(d => d.valor);
        this.createChartOptions(valores, categorias);
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
        type: "category",
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

  exportarNivel(): void {
    this.reportService.exportarNivelXLS(3, this.filtros?.tipoMedicao, this.filtros?.data, this.filtros?.dataInicio, this.filtros?.dataFim, this.filtros?.dias)
    .subscribe({
      next: (response) => {
        const contentDisposition = response.headers.get('Content-Disposition');
        const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
        const filename = filenameMatch ? filenameMatch[1] : 'relatorio_nivel.xlsx';

        saveAs(response.body!, filename);
      },
      error: (err) => console.error('Erro ao exportar:', err)
    });
  }

}

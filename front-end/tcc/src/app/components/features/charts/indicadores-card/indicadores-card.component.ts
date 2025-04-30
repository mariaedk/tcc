import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { ResultadoAnaliseSchema } from 'src/app/models/ResultadoAnaliseSchema';
import { TipoConsulta } from 'src/app/models/TipoConsulta';
import { AnaliseService } from 'src/app/services/analise/analise.service';

@Component({
  selector: 'app-indicadores-card',
  templateUrl: './indicadores-card.component.html',
  styleUrls: ['./indicadores-card.component.scss']
})
export class IndicadoresCardComponent implements OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();
  metricas: any;

  constructor(private analiseService: AnaliseService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados(): void {
    if ((this.filtros.dataInicio && !this.filtros.dataFim) || (!this.filtros.dataInicio && this.filtros.dataFim)) return;

    const commonCallback = (res: ResultadoAnaliseSchema) => {
      if (res.dados_insuficientes) {
        this.metricas = {
          ultimoValor: {
            valor: 0,
            data: '--'
          },
          maximo: {
            valor: 0,
            data: '--'
          },
          minimo: {
            valor: 0,
            data: '--'
          },
          anomalias: {
            qtd: 0,
            periodo: `Quantidade de registros insuficiente.`
          }
        };
      } else {
        this.metricas = {
          ultimoValor: {
            valor: res.ultimo_valor?.toFixed(2),
            data: res.data_fim
          },
          maximo: {
            valor: res.maximo?.toFixed(2),
            data: res.data_inicio
          },
          minimo: {
            valor: res.minimo?.toFixed(2),
            data: res.data_inicio
          },
          anomalias: {
            qtd: res.anomalias,
            periodo: `nos últimos ${res.total_medicoes} registros`
          }
        };
      }

      setTimeout(() => this.chartLoaded.emit());
    };

    if (this.filtros?.tipoConsulta === TipoConsulta.MEDIA) {
      this.analiseService.getAnaliseAutomatica(
        3,
        this.filtros?.dias,
        this.filtros?.data,
        this.filtros?.dataInicio,
        this.filtros?.dataFim
      ).subscribe(commonCallback);
    }

    if (this.filtros?.tipoConsulta === TipoConsulta.HORA) {
      this.analiseService.getAnaliseAutomaticaHora(
        3,
        this.filtros?.data
      ).subscribe(commonCallback);
    }
  }


}

import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { ResultadoAnaliseSchema } from 'src/app/models/ResultadoAnaliseSchema';
import { AnaliseService } from 'src/app/services/analise/analise.service';

@Component({
  selector: 'app-indicadores-card',
  templateUrl: './indicadores-card.component.html',
  styleUrls: ['./indicadores-card.component.scss']
})
export class IndicadoresCardComponent implements OnChanges, OnInit {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();
  metricas: any;

  constructor(private analiseService: AnaliseService) {}

  ngOnInit(): void {

  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados(): void {

    if ((this.filtros.dataInicio && !this.filtros.dataFim) || (!this.filtros.dataInicio && this.filtros.dataFim)) {
      return;
    }

    this.analiseService.getAnaliseAutomatica(
      3,
      this.filtros?.dias,
      this.filtros?.data,
      this.filtros?.dataInicio,
      this.filtros?.dataFim
    ).subscribe((res: ResultadoAnaliseSchema) => {
      this.metricas = {
        ultimoValor: {
          valor: res.ultimo_valor?.toFixed(2),
          data: res.data_fim || '--'
        },
        maximo: {
          valor: res.maximo?.toFixed(2),
          data: res.data_inicio || '--'
        },
        minimo: {
          valor: res.minimo?.toFixed(2),
          data: res.data_inicio || '--'
        },
        anomalias: {
          qtd: res.anomalias,
          periodo: `nos últimos ${res.total_medicoes} registros`
        }

      };
      setTimeout(() => {
        this.chartLoaded.emit();
      });
    });
  }
}

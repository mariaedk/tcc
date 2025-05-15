import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { ResultadoAnaliseSchema } from 'src/app/models/ResultadoAnaliseSchema';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
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
    if (TipoMedicao.DIA == this.filtros.tipoMedicao && ((this.filtros.dataInicio && !this.filtros.dataFim) || (!this.filtros.dataInicio && this.filtros.dataFim)
      || (!this.filtros.dataInicio && !this.filtros.dataFim && !this.filtros.dias))) {
      return;
    }

    if (TipoMedicao.HORA == this.filtros.tipoMedicao && (!this.filtros.data)) {
      return;
    }

    if (this.filtros.dataInicio && this.filtros.dataFim && this.filtros.dias) {
      this.filtros.dias = null;
    }

    const formatadorDataCompleta: Intl.DateTimeFormatOptions = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    };


    const formatadorDataSimples: Intl.DateTimeFormatOptions = {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    };

    const commonCallback = (res: ResultadoAnaliseSchema) => {
      const formatarData = (dataStr: string) =>
        new Date(dataStr).toLocaleString('pt-BR', this.filtros?.tipoMedicao === TipoMedicao.HORA ? formatadorDataCompleta : formatadorDataSimples);

      this.metricas = {
        ultimoValor: {
          valor: res.ultimo_valor?.toFixed(2),
          data: formatarData(res.data_fim)
        },
        maximo: {
          valor: res.maximo?.toFixed(2),
          data: formatarData(res.data_inicio)
        },
        minimo: {
          valor: res.minimo?.toFixed(2),
          data: formatarData(res.data_inicio)
        },
        anomalias: {
          qtd: res.anomalias,
          periodo: `nos últimos ${res.total_medicoes} registros`
        }
      };

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
        const formatarData = (dataStr: string) =>
          new Date(dataStr).toLocaleString('pt-BR', this.filtros?.tipoMedicao === TipoMedicao.HORA ? formatadorDataSimples : formatadorDataCompleta);

        this.metricas = {
          ultimoValor: {
            valor: res.ultimo_valor?.toFixed(2),
            data: formatarData(res.data_fim)
          },
          maximo: {
            valor: res.maximo?.toFixed(2),
            data: formatarData(res.data_inicio)
          },
          minimo: {
            valor: res.minimo?.toFixed(2),
            data: formatarData(res.data_inicio)
          },
          anomalias: {
            qtd: res.anomalias,
            periodo: `nos últimos ${res.total_medicoes} registros`
          }
        };
      }

      setTimeout(() => this.chartLoaded.emit());
    };

    if (this.filtros?.tipoMedicao === TipoMedicao.DIA) {
      this.analiseService.getAnaliseAutomaticaGeral(
        3,
        this.filtros?.dias,
        this.filtros?.data,
        this.filtros?.dataInicio,
        this.filtros?.dataFim
      ).subscribe(commonCallback);
    }

    if (this.filtros?.tipoMedicao === TipoMedicao.HORA) {
      this.analiseService.getAnaliseAutomaticaHora(
        3,
        this.filtros?.data
      ).subscribe(commonCallback);
    }
  }


}

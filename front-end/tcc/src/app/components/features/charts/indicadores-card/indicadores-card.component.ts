import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { AnaliseService } from 'src/app/services/analise/analise.service';
import { TipoMedicao } from 'src/app/models/TipoMedicao';
import { ResultadoAnaliseSchema } from 'src/app/models/ResultadoAnaliseSchema';

@Component({
  selector: 'app-indicadores-card',
  templateUrl: './indicadores-card.component.html',
  styleUrls: ['./indicadores-card.component.scss']
})
export class IndicadoresCardComponent implements OnChanges {

  @Input() filtros: any;
  @Input() sensor: any;
  @Output() chartLoaded = new EventEmitter<void>();

  cards: any[] = [];

  constructor(private analiseService: AnaliseService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados(): void {
    const { data, dataInicio, dataFim, dias, tipoMedicao } = this.filtros;
    const incluirHora = tipoMedicao === TipoMedicao.HORA;

    // Bloqueia envio com datas incompletas
    if ((dataInicio && !dataFim) || (!dataInicio && dataFim)) return;

    // Impede chamadas com filtros inválidos
    const filtrosInvalidos =
      (tipoMedicao === TipoMedicao.HORA && !data) ||
      (tipoMedicao === TipoMedicao.DIA && !dias && !(dataInicio && dataFim)) ||
      (tipoMedicao === TipoMedicao.INST && !data && !(dataInicio && dataFim));

    if (filtrosInvalidos) {
      this.chartLoaded.emit();
      return;
    }

    // Continua se os filtros estiverem válidos
    this.analiseService.getAnaliseAutomatica(
      this.sensor,
      tipoMedicao,
      dias,
      this.formatarData(data),
      this.formatarData(dataInicio),
      this.formatarData(dataFim)
    ).subscribe((res: ResultadoAnaliseSchema) => {
      const formatar = (data: string) => this.formatarDataExibicao(data, incluirHora);
      const unidade = res.unidade ?? '';

      if (res.dados_insuficientes) {
        this.montarCards('--', '--', '--', 0, 'Quantidade de registros insuficiente.', unidade);
      } else {
        this.montarCards(
          res.ultimo_valor?.toFixed(2) ?? '--',
          res.maximo?.toFixed(2) ?? '--',
          res.minimo?.toFixed(2) ?? '--',
          res.anomalias,
          res.total_medicoes ? `nos últimos ${res.total_medicoes} registros` : 'Sem registros',
          unidade,
          formatar(res.data_fim),
          formatar(res.data_inicio)
        );
      }

      setTimeout(() => this.chartLoaded.emit(), 100);
    });
  }

  montarCards(
    ultimo: string,
    maximo: string,
    minimo: string,
    anomalias: number,
    periodo: string,
    unidade: string,
    dataUltimo: string = '--',
    dataInicio: string = '--'
  ) {
    this.cards = [
      {
        icon: '⏱️',
        title: 'Último Valor Medido',
        value: ultimo,
        unit: unidade,
        subtitle: `em ${dataUltimo}`,
        color: 'primary'
      },
      {
        icon: '📈',
        title: 'Valor Máximo',
        value: maximo,
        unit: unidade,
        subtitle: `desde ${dataInicio}`,
        color: 'success'
      },
      {
        icon: '📉',
        title: 'Valor Mínimo',
        value: minimo,
        unit: unidade,
        subtitle: `desde ${dataInicio}`,
        color: 'info'
      }
    ];
  }

  formatarDataExibicao(dataStr: string | null | undefined, incluirHora = false): string {
    if (!dataStr) return '--';
    const data = new Date(dataStr);
    if (isNaN(data.getTime())) return '--';

    const options: Intl.DateTimeFormatOptions = incluirHora
      ? { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }
      : { day: '2-digit', month: '2-digit', year: 'numeric' };

    return data.toLocaleString('pt-BR', options);
  }

  formatarData(data: string | Date | null | undefined): string | undefined {
    if (!data) return undefined;
    const d = new Date(data);
    return isNaN(d.getTime()) ? undefined : d.toISOString();
  }
}

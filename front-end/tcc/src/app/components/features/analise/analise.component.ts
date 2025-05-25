import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { AnaliseService } from 'src/app/services/analise/analise.service';

@Component({
  selector: 'app-analise',
  templateUrl: './analise.component.html',
  styleUrls: ['./analise.component.scss']
})
export class AnaliseComponent implements OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  message: string = "";

  constructor(private analiseService: AnaliseService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  carregarDados() {
    const { data, dataInicio, dataFim, dias, tipoMedicao } = this.filtros;

    if ((dataInicio && !dataFim) || (!dataInicio && dataFim)) return;

    this.analiseService.getAnaliseAutomatica(
      1, // ID do sensor
      tipoMedicao,
      dias,
      this.formatarData(data),
      this.formatarData(dataInicio),
      this.formatarData(dataFim)
    ).subscribe(resp => {
      if (resp) {
        this.message = resp.mensagem;
        setTimeout(() => this.chartLoaded.emit());
      }
    });
  }

  private formatarData(data: string | Date | null | undefined): string | undefined {
    if (!data) return undefined;
    const d = new Date(data);
    return isNaN(d.getTime()) ? undefined : d.toISOString();
  }
}

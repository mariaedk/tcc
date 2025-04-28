import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-filtros',
  templateUrl: './filtros.component.html',
  styleUrls: ['./filtros.component.scss']
})
export class FiltrosComponent {

  @Output() filtrosAtualizados = new EventEmitter<any>();

  tipoConsulta: 'geral' | 'media' = 'media';
  data?: string;
  dataInicio?: string;
  dataFim?: string;
  // por padrão trazer 20 dias
  dias?: number = 20

  constructor() {}

  ngOnInit() {
    this.filtrosAtualizados.emit({
      tipoConsulta: this.tipoConsulta,
      data: this.data,
      dias: this.dias,
      dataInicio: this.dataInicio,
      dataFim: this.dataFim
    });
  }

  buscar() {
    this.filtrosAtualizados.emit({
      tipoConsulta: this.tipoConsulta,
      data: this.data,
      dias: this.dias,
      dataInicio: this.dataInicio,
      dataFim: this.dataFim
    });
  }

}

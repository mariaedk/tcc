import { Component, EventEmitter, Output, AfterViewInit } from '@angular/core';
import { TipoMedicao } from 'src/app/models/TipoMedicao';

@Component({
  selector: 'app-filtros',
  templateUrl: './filtros.component.html',
  styleUrls: ['./filtros.component.scss']
})
export class FiltrosComponent {

  @Output() filtrosAtualizados = new EventEmitter<any>();

  dataMaximaHoje: string = new Date().toISOString().split('T')[0];
  TipoMedicao = TipoMedicao;
  tipo = TipoMedicao.DIA;
  data?: string;
  dataInicio?: string;
  dataFim?: string;
  dias?: number = 20

  constructor() {}

  ngOnInit() {
    this.filtrosAtualizados.emit({
      tipoMedicao: this.tipo,
      data: this.data,
      dias: this.dias,
      dataInicio: this.dataInicio,
      dataFim: this.dataFim
    });
  }

  limparFiltros() {
    this.tipo = TipoMedicao.DIA
    this.data = undefined;
    this.dataInicio = undefined;
    this.dataFim = undefined;
    this.dias = 20;

    this.filtrosAtualizados.emit({
      tipoMedicao: this.tipo,
      data: this.data,
      dias: this.dias,
      dataInicio: this.dataInicio,
      dataFim: this.dataFim
    });
  }


  buscar() {
    if (this.dataInicio && this.dataFim) {
      this.dias = undefined;
    }

    if (this.dias && (!this.dataInicio || !this.dataFim)) {
      this.dataInicio = undefined;
      this.dataFim = undefined;
    }

    this.filtrosAtualizados.emit({
      tipoMedicao: this.tipo,
      data: this.data,
      dias: this.dias,
      dataInicio: this.dataInicio,
      dataFim: this.dataFim
    });
  }


  updateCampos() {
    if (this.tipo === TipoMedicao.HORA) {
      this.data = undefined;
      this.dataInicio = undefined;
      this.dataFim = undefined;
      this.dias = undefined;
    }

    if (this.tipo === TipoMedicao.DIA) {
      this.data = undefined;
      this.dataInicio = undefined;
      this.dataFim = undefined;
      this.dias = 20;
    }

    this.buscar();
  }

}

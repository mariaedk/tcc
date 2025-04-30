
import { Component, EventEmitter, Output } from '@angular/core';
import { TipoConsulta } from 'src/app/models/TipoConsulta';

@Component({
  selector: 'app-filtros',
  templateUrl: './filtros.component.html',
  styleUrls: ['./filtros.component.scss']
})
export class FiltrosComponent {

  @Output() filtrosAtualizados = new EventEmitter<any>();

  TipoConsulta = TipoConsulta; // expõe o enum pro HTML
  tipo = TipoConsulta.MEDIA;
  data?: string;
  dataInicio?: string;
  dataFim?: string;
  dias?: number = 20

  constructor() {}

  ngOnInit() {
    this.filtrosAtualizados.emit({
      tipoConsulta: this.tipo,
      data: this.data,
      dias: this.dias,
      dataInicio: this.dataInicio,
      dataFim: this.dataFim
    });
  }

  buscar() {
    this.filtrosAtualizados.emit({
      tipoConsulta: this.tipo,
      data: this.data,
      dias: this.dias,
      dataInicio: this.dataInicio,
      dataFim: this.dataFim
    });
  }

  updateCampos() {
    if (this.tipo === TipoConsulta.HORA) {
      this.data = undefined;
      this.dataInicio = undefined;
      this.dataFim = undefined;
      this.dias = undefined;
    }

    if (this.tipo === TipoConsulta.MEDIA) {
      this.data = undefined;
      this.dataInicio = undefined;
      this.dataFim = undefined;
      this.dias = 20; // reseta para 20 dias padrão
    }
  }

}

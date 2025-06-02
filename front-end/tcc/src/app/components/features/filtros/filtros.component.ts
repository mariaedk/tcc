import { Component, EventEmitter, Output } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TipoMedicao } from 'src/app/models/TipoMedicao';

@Component({
  selector: 'app-filtros',
  templateUrl: './filtros.component.html',
  styleUrls: ['./filtros.component.scss']
})
export class FiltrosComponent {

  @Output() filtrosAtualizados = new EventEmitter<any>();

  TipoMedicao = TipoMedicao;
  tipo = TipoMedicao.DIA;

  data?: Date;
  dataInicio?: Date;
  dataFim?: Date;
  dias?: number = 20;

  dataMaximaHoje = new Date();

  constructor(private snackbar: MatSnackBar) {}

  ngOnInit() {
    this.emitirFiltros();
  }

  emitirFiltros() {
    this.filtrosAtualizados.emit({
      tipoMedicao: this.tipo,
      data: this.data,
      dias: this.dias,
      dataInicio: this.dataInicio,
      dataFim: this.dataFim
    });
  }

  buscar() {
    const hoje = new Date();

    if (this.data && this.data > hoje) this.data = hoje;
    if (this.dataInicio && this.dataInicio > hoje) this.dataInicio = hoje;
    if (this.dataFim && this.dataFim > hoje) this.dataFim = hoje;

    if (this.dataInicio && this.dataFim && this.dataFim < this.dataInicio) {
      this.dataFim = this.dataInicio;
    }

    if (this.tipo === TipoMedicao.HORA) {
      this.dataInicio = undefined;
      this.dataFim = undefined;
      this.dias = undefined;
      this.emitirFiltros();
      return;
    }

    if (this.tipo === TipoMedicao.INST) {
      const filtrosUsados = [
        !!this.data,
        !!this.dias,
        !!this.dataInicio || !!this.dataFim
      ].filter(Boolean).length;

      if (this.dataFim && !this.dataInicio) {
        return;
      }

      if (filtrosUsados > 1) {
        this.data = undefined;
        this.dataInicio = undefined;
        this.dataFim = undefined;
        this.dias = undefined;
        this.snackbar.open('Somente intervalo de datas pode ser usado nas medições instantâneas.', 'Fechar', {
          duration: 3000
        });
        this.emitirFiltros();
        return;
      }

      if (!this.dataInicio && !this.dataFim) {
        this.snackbar.open('Preencha a data de início e a data de fim para visualizar medições instantâneas.', 'Fechar', {
          duration: 3000
        });
        return;
      }

      const diff = (this.dataFim!.getTime() - this.dataInicio!.getTime()) / (1000 * 60 * 60 * 24);
      if (diff > 5) {
        this.snackbar.open('O intervalo não pode ultrapassar 5 dias em medições instantâneas.', 'Fechar', {
          duration: 3000
        });
        return;
      }

      this.emitirFiltros();
      return;
    }

    if (this.tipo === TipoMedicao.DIA) {
      if (this.dataInicio && !this.dataFim) {
        this.dias = undefined;
        return;
      }

      if (this.dataFim && !this.dataInicio) {
        return;
      }

      if (this.dias) {
        this.dataInicio = undefined;
        this.dataFim = undefined;
      }

      if (this.dataInicio && this.dataFim) {
        this.dias = undefined;
      }

      this.emitirFiltros();
      return;
    }

    this.emitirFiltros();
  }

  onDataInicioChange() {
    if (this.tipo === TipoMedicao.DIA || this.tipo === TipoMedicao.INST) {
      if (this.dataFim) {
        this.dataFim = undefined;
        this.dias = undefined;
      }
    }
    this.buscar();
  }

  limparFiltros() {
    this.tipo = TipoMedicao.DIA;
    this.data = undefined;
    this.dataInicio = undefined;
    this.dataFim = undefined;
    this.dias = 20;
    this.emitirFiltros();
  }

  updateCampos() {
    this.data = undefined;
    this.dataInicio = undefined;
    this.dataFim = undefined;
    this.dias = this.tipo === TipoMedicao.DIA ? 20 : undefined;
    this.buscar();
  }
}

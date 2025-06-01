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

    if (this.tipo === TipoMedicao.DIA && ((!this.dataInicio && this.dataFim) || (this.dataInicio && !this.dataFim) || (this.dataInicio && this.dataFim))) {
      this.dias = undefined;
    }

    if (this.tipo === TipoMedicao.INST) {
      if ((!this.dataInicio && !this.dataFim)) {
        this.snackbar.open('Preencha a data de início e data de fim antes de buscar medições instântaneas.', 'Fechar', {
            duration: 3000
          });
        return;
      }

      if ((!this.dataInicio && this.dataFim) || (this.dataInicio && !this.dataFim)) {
        return;
      }

      const inicio = new Date(this.dataInicio!);
      const fim = new Date(this.dataFim!);

      const diffEmMs = fim.getTime() - inicio.getTime();
      const diffEmDias = diffEmMs / (1000 * 60 * 60 * 24);

      if (diffEmDias > 30) {
        this.snackbar.open('O intervalo não pode ser superior a 30 dias.', 'Fechar', {
          duration: 3000
        });
        return;
      }

      // só um filtro por vez
      const filtrosPreenchidos = [
        !!this.data,
        !!this.dias,
        !!this.dataInicio || !!this.dataFim
      ].filter(v => v).length;

      if (filtrosPreenchidos > 1) {
        this.data = undefined;
        this.dataInicio = undefined;
        this.dataFim = undefined;
        this.dias = undefined;
      }
    }

    if (this.tipo === TipoMedicao.HORA) {
      this.dataInicio = undefined;
      this.dataFim = undefined;
      this.dias = undefined;
    }

    if (this.tipo === TipoMedicao.DIA) {
      if (this.dataInicio && this.dataFim) {
        this.dias = undefined;
      }
      if (this.dias && (!this.dataInicio || !this.dataFim)) {
        this.dataInicio = undefined;
        this.dataFim = undefined;
      }
    }

    this.emitirFiltros();
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

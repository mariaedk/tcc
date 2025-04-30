import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { TipoConsulta } from 'src/app/models/TipoConsulta';
import { AnaliseService } from 'src/app/services/analise/analise.service';

@Component({
  selector: 'app-analise',
  templateUrl: './analise.component.html',
  styleUrls: ['./analise.component.scss']
})
export class AnaliseComponent implements OnInit, OnChanges {

  @Input() filtros: any;
  @Output() chartLoaded = new EventEmitter<void>();

  message: string = "";


  constructor(private analiseService: AnaliseService) {

  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['filtros'] && changes['filtros'].currentValue) {
      this.carregarDados();
    }
  }

  ngOnInit() {
    // this.carregarDados();
  }

  carregarDados() {

    if ((this.filtros.dataInicio && !this.filtros.dataFim) || (!this.filtros.dataInicio && this.filtros.dataFim)) {
      return;
    }

    if (this.filtros?.tipoConsulta == TipoConsulta.MEDIA) {
      this.analiseService.getAnaliseAutomatica(3, this.filtros?.dias).subscribe(resp => {
        if (resp) {
          this.message = resp.mensagem;

          setTimeout(() => {
            this.chartLoaded.emit();
          });
        }
      });
    }

    if (this.filtros?.tipoConsulta == TipoConsulta.HORA) {
      this.analiseService.getAnaliseAutomaticaHora(3, this.filtros?.data).subscribe(resp => {
        if (resp) {
          this.message = resp.mensagem;

          setTimeout(() => {
            this.chartLoaded.emit();
          });
        }
      });
    }
  }

}

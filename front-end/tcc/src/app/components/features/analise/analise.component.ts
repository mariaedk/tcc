import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
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
    this.carregarDados();
  }

  carregarDados() {
    this.analiseService.getAnaliseAutomatica(3, this.filtros?.dias).subscribe(resp => {
      if (resp) {
        this.message = resp.mensagem;

        setTimeout(() => {
          this.chartLoaded.emit();
        });
      }
    });
  }

}

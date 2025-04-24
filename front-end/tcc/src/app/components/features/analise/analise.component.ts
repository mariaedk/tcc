import { Component, OnInit } from '@angular/core';
import { AnaliseService } from 'src/app/services/analise/analise.service';

@Component({
  selector: 'app-analise',
  templateUrl: './analise.component.html',
  styleUrls: ['./analise.component.scss']
})
export class AnaliseComponent implements OnInit {

  message: string = "";

  constructor(private analiseService: AnaliseService) {

  }

  ngOnInit() {
    this.analiseService.getAnaliseAutomatica(3, 20).subscribe(resp => {
      if (resp) {
        this.message = resp.mensagem;
      }
    });
  }

}

import { Component } from '@angular/core';
import { FiltroData } from 'src/app/models/FiltroData';
import { AnaliseService } from 'src/app/services/analise/analise.service';
import { MedicaoService } from 'src/app/services/medicao/medicao.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  chartsToLoad = 4;
  loadedCharts = 0;
  loading = true;
  filtros: any;

  constructor() {}

  ngOnInit() {
  }

  onFiltrosAtualizados(filtros: any) {
    this.filtros = filtros;
    this.loadedCharts = 0; 
    this.loading = true;
  }

  onChartLoaded() {
    this.loadedCharts++;
    if (this.loadedCharts >= this.chartsToLoad) {
       this.loading = false;
    }
  }

}

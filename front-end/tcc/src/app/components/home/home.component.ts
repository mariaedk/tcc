import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent {

  chartsToLoad = 3;
  loadedCharts = 0;
  loading = true;

  constructor() {

  }

  ngOnInit() {
  }


  onChartLoaded() {
    this.loadedCharts++;
    if (this.loadedCharts >= this.chartsToLoad) {
      this.loading = false;
    }
  }

}

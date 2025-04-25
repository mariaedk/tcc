import { NgModule } from '@angular/core';
import { HeaderComponent } from './comum/header/header.component';
import { FooterComponent } from './comum/footer/footer.component';
import { CommonModule } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from '../app-routing.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HomeComponent } from './home/home.component';
import { NgApexchartsModule } from 'ng-apexcharts';
import { LineChartComponent } from './features/charts/line-chart/line-chart.component';
import { AreaChartComponent } from './features/charts/area-chart/area-chart.component';
import { AnaliseComponent } from './features/analise/analise.component';
import { VerticalBarChartComponent } from './features/charts/vertical-bar-chart/vertical-bar-chart.component';
import { LineMarkerChartComponent } from './features/charts/line-marker-chart/line-marker-chart.component';

@NgModule({
  declarations: [
    HeaderComponent,
    FooterComponent,
    LoginComponent,
    HomeComponent,
    LineChartComponent,
    AreaChartComponent,
    AnaliseComponent,
    VerticalBarChartComponent,
    LineMarkerChartComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    NgApexchartsModule
  ],
  exports: [
    HeaderComponent,
    FooterComponent,
    LoginComponent
  ]
})
export class SharedModule { }

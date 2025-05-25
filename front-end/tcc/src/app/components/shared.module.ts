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
import { LineMarkerChartComponent } from './features/charts/line-marker-chart/line-marker-chart.component';
import { IndicadoresCardComponent } from './features/charts/indicadores-card/indicadores-card.component';
import { FiltrosComponent } from './features/filtros/filtros.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { MatSelectModule } from '@angular/material/select';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBarModule } from '@angular/material/snack-bar';

@NgModule({
  declarations: [
    HeaderComponent,
    FooterComponent,
    LoginComponent,
    HomeComponent,
    LineChartComponent,
    AreaChartComponent,
    AnaliseComponent,
    LineMarkerChartComponent,
    IndicadoresCardComponent,
    FiltrosComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
    NgApexchartsModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatIconModule,
    MatSelectModule,
    MatTooltipModule,
    MatButtonModule,
    MatSnackBarModule
  ],
  exports: [
    HeaderComponent,
    FooterComponent,
    LoginComponent
  ]
})
export class SharedModule { }

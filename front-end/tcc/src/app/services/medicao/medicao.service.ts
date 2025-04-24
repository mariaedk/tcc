import { environment } from './../../../environments/.environment';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ComparativoVazaoResponseSchema } from 'src/app/models/ComparativoVazaoResponseSchema';
import { MedicaoHistoricoSchema } from 'src/app/models/MedicaoHistoricoSchema';

@Injectable({
  providedIn: 'root'
})
export class MedicaoService {

  public apiUrl = environment.apiUrl + "/medicao";

  constructor(private http: HttpClient) { }

  getHistoricoSensor(codigoSensor: number, dias: number): Observable<MedicaoHistoricoSchema[]> {
    return this.http.get<MedicaoHistoricoSchema[]>(`${this.apiUrl}/historico-data/sensor/${codigoSensor}/${dias}`);
  }

  getCompararVazoesPorMes(codigoSensorEntrada: number, codigoSensorSaida: number, meses: number): Observable<ComparativoVazaoResponseSchema> {
    return this.http.get<ComparativoVazaoResponseSchema>(`${this.apiUrl}/vazoes-mes/${codigoSensorEntrada}/${codigoSensorSaida}/${meses}`);
  }

}

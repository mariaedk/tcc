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

  buscarGeral(sensorCodigo: number, data?: string, dataInicio?: string, dataFim?: string, dias?: number) {
    const params: any = {};
    if (data) params.data = data;
    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;
    if (dias) params.dias = dias;

    return this.http.get<MedicaoHistoricoSchema[]>(`${this.apiUrl}/geral/${sensorCodigo}`, { params });
  }

  buscarPorHora(sensorCodigo: number, data: string) {
    const params = { data };
    return this.http.get<MedicaoHistoricoSchema[]>(`${this.apiUrl}/media-por-hora/${sensorCodigo}`, { params });
  }

  buscarMediaPorDia(sensorCodigo: number, data?: string, dataInicio?: string, dataFim?: string, dias?: number) {
    const params: any = {};
    if (data) params.data = data;
    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;
    if (dias) params.dias = dias;

    return this.http.get<MedicaoHistoricoSchema[]>(`${this.apiUrl}/media-por-dia/${sensorCodigo}`, { params });
  }

  getCompararVazoesPorMes(
    codigoSensorEntrada: number,
    codigoSensorSaida: number,
    meses: number = 6,
    dataInicio?: string,
    dataFim?: string
  ): Observable<ComparativoVazaoResponseSchema> {
    let params: any = { meses };

    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;

    return this.http.get<ComparativoVazaoResponseSchema>(
      `${this.apiUrl}/vazoes-mes/${codigoSensorEntrada}/${codigoSensorSaida}`,
      { params }
    );
  }

}

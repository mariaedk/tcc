import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ReportService {

  public apiUrl = environment.apiUrl + "/report";

  constructor(private httpClient: HttpClient) { }

  exportarVazao2XLS(sensorCodigo: number, tipoMedicao: string, data?: string, dataInicio?: string, dataFim?: string, dias?: number) {
    const params: any = {
      tipo_medicao: tipoMedicao,
      sensor_codigo: sensorCodigo,
    };

    if (data) params.data = data;
    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;
    if (dias) params.dias = dias;

    return this.httpClient.get(`${this.apiUrl}/vazao2/export/xls`, {
      params,
      observe: 'response',
      responseType: 'blob'
    });
  }

  exportarVazaoXLS(sensorCodigo: number, tipoMedicao: string, data?: string, dataInicio?: string, dataFim?: string, dias?: number) {
    let params: any = {}

    params.tipo_medicao = tipoMedicao
    params.sensor_codigo = sensorCodigo

    if (data) params.data = data;
    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;
    if (dias) params.dias = dias;


    return this.httpClient.get(`${this.apiUrl}/vazao/export/xls`, {
      params,
      observe: 'response',
      responseType: 'blob'
    });
  }

  exportarAnomaliaXLS(sensorCodigo: number, tipoMedicao: string, data?: string, dataInicio?: string, dataFim?: string, dias?: number) {
    let params: any = {}

    params.tipo_medicao = tipoMedicao
    params.sensor_codigo = sensorCodigo

    if (data) params.data = data;
    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;
    if (dias) params.dias = dias;


    return this.httpClient.get(`${this.apiUrl}/analise/anomalia/export/xls`, {
      params,
      observe: 'response',
      responseType: 'blob'
    });
  }

  exportarVazao2PDF(sensorCodigo: number, tipoMedicao: string, data?: string, dataInicio?: string, dataFim?: string, dias?: number) {
    let params: any = {}

    params.tipo_medicao = tipoMedicao
    params.sensor_codigo = sensorCodigo

    if (data) params.data = data;
    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;
    if (dias) params.dias = dias;

    return this.httpClient.get(`${this.apiUrl}/vazao2/export/pdf`, {
      params,
      observe: 'response',
      responseType: 'blob'
    });
  }

  exportarVazaoPDF(sensorCodigo: number, tipoMedicao: string, data?: string, dataInicio?: string, dataFim?: string, dias?: number) {
    let params: any = {}

    params.tipo_medicao = tipoMedicao
    params.sensor_codigo = sensorCodigo

    if (data) params.data = data;
    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;
    if (dias) params.dias = dias;

    return this.httpClient.get(`${this.apiUrl}/vazao/export/pdf`, {
      params,
      observe: 'response',
      responseType: 'blob'
    });
  }

  exportarAnomaliaPDF(sensorCodigo: number, tipoMedicao: string, data?: string, dataInicio?: string, dataFim?: string, dias?: number) {
    let params: any = {}

    params.tipo_medicao = tipoMedicao
    params.sensor_codigo = sensorCodigo

    if (data) params.data = data;
    if (dataInicio) params.data_inicio = dataInicio;
    if (dataFim) params.data_fim = dataFim;
    if (dias) params.dias = dias;

    return this.httpClient.get(`${this.apiUrl}/analise/anomalia/export/pdf`, {
      params,
      observe: 'response',
      responseType: 'blob'
    });
  }


}

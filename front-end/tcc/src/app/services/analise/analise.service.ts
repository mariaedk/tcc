import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from './../../../environments/.environment';
import { ResultadoAnaliseSchema } from 'src/app/models/ResultadoAnaliseSchema';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AnaliseService {

  public apiUrl = environment.apiUrl + "/analise";

  constructor(private http: HttpClient) { }

  getAnaliseAutomatica(
    cd_sensor: number,
    dias?: number,
    data?: string,
    data_inicio?: string,
    data_fim?: string
  ): Observable<any> {
    let params = '';

    if (data) {
      params = `?data=${data}`;
    } else if (data_inicio && data_fim) {
      params = `?data_inicio=${data_inicio}&data_fim=${data_fim}`;
    } else if (dias) {
      params = `?dias=${dias}`;
    }

    return this.http.get<any>(`${this.apiUrl}/nivel/sensor/${cd_sensor}${params}`);
  }
}

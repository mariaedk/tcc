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

  getAnaliseAutomatica(cd_sensor: number, dias?: number): Observable<ResultadoAnaliseSchema> {
    let url = `${this.apiUrl}/nivel/sensor/${cd_sensor}`;
    if (dias) {
      url += `?dias=${dias}`
    }
    return this.http.get<ResultadoAnaliseSchema>(url);
  }

}

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UnidadeMedidaService {

  public apiUrl = environment.apiUrl + "/medicao";

  constructor(private http: HttpClient) { }

  

}

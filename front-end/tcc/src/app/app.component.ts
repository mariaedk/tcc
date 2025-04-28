import { Component } from '@angular/core';
import { AuthService } from './services/auth/auth.service';
import { registerLocaleData } from '@angular/common';
import localePt from '@angular/common/locales/pt';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'tcc';

  constructor(public authService: AuthService) {}


  ngOnInit() {
    registerLocaleData(localePt, 'pt-BR');
  }

}

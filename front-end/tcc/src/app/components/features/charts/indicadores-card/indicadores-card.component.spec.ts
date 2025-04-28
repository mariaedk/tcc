import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IndicadoresCardComponent } from './indicadores-card.component';

describe('IndicadoresCardComponent', () => {
  let component: IndicadoresCardComponent;
  let fixture: ComponentFixture<IndicadoresCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IndicadoresCardComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IndicadoresCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

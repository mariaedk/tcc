import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LineMarkerChartComponent } from './line-marker-chart.component';

describe('LineMarkerChartComponent', () => {
  let component: LineMarkerChartComponent;
  let fixture: ComponentFixture<LineMarkerChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LineMarkerChartComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LineMarkerChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

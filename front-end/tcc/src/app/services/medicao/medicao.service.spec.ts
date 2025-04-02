import { TestBed } from '@angular/core/testing';

import { MedicaoService } from './medicao.service';

describe('MedicaoService', () => {
  let service: MedicaoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MedicaoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

"""from time import timezone

@author maria
date: 2025-02-23
"""
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from datetime import date

class MedicaoBase(BaseModel):
    sensor_id: int
    unidade_id: int
    valor: Optional[float] = None
    valor_str: Optional[str] = None
    valor_bool: Optional[bool] = None

class MedicaoCreate(MedicaoBase):
    pass

class MedicaoResponse(MedicaoBase):
    id: int
    data_hora: datetime
    coleta_id: int

    class Config:
        from_attributes = True

class MedicaoHistoricoSchema(BaseModel):
    data: datetime
    valor: float

class SerieComparativaSchema(BaseModel):
    name: str
    data: list[float]

class ComparativoVazaoResponseSchema(BaseModel):
    categorias: list[str]
    series: list[SerieComparativaSchema]
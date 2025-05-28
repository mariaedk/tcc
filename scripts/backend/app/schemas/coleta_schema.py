"""
@author maria
date: 2025-04-17
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.schemas.medicao_schema import MedicaoCreate, MedicaoResponse

class ColetaBase(BaseModel):
    origem: Optional[str] = None

class ColetaCreate(ColetaBase):
    origem: Optional[str] = "CLP"
    data_hora: datetime
    medicoes: list[MedicaoCreate]

class ColetaResponse(ColetaBase):
    id: int
    data_hora: datetime
    medicoes: List[MedicaoResponse]

    class Config:
        from_attributes = True
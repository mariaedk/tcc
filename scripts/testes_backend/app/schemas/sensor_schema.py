"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel
from app.schemas.enums_schema import TipoSensor

class SensorBase(BaseModel):
    nome: str
    tipo: TipoSensor
    dispositivo_id: int

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    id: int

    class Config:
        orm_mode = True
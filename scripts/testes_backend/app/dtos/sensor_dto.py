"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel
from app.dtos.enums_dto import TipoSensor

class SensorDTO(BaseModel):
    id: int
    nome: str
    tipo: TipoSensor
    dispositivo_id: int

    class Config:
        orm_mode = True

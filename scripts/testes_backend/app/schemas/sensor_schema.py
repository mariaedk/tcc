"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, Field
from app.schemas.enums_schema import TipoSensor
import app.length_constants as length_constants

class SensorBase(BaseModel):
    nome: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    tipo: TipoSensor
    dispositivo_id: int

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    id: int

    class Config:
        from_attributes = True

class SensorUpdate(BaseModel):
    id: int | None = None
    nome: str | None = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    dispositivo_id: int | None
    tipo: TipoSensor | None = None
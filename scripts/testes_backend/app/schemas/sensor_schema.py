"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, Field, field_validator
from app.models.enums import TipoSensor
import app.length_constants as length_constants
from typing import Optional

class SensorBase(BaseModel):
    nome: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    tipo: TipoSensor
    dispositivo_id: int

    @field_validator("tipo", mode="before")
    @classmethod
    def validar_tipo(cls, v):
        if isinstance(v, TipoSensor):
            return v.value
        return v

class SensorCreate(SensorBase):
    pass

class SensorResponse(SensorBase):
    id: int

    class Config:
        from_attributes = True

class SensorUpdate(BaseModel):
    id: int
    nome: Optional[str] = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    dispositivo_id: Optional[int] = None
    tipo: Optional[TipoSensor] = None

    class Config:
        from_attributes = True
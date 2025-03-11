"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, Field, field_validator
from app.models.enums import TipoDispositivo
import app.length_constants as length_constants
from typing import Optional

class DispositivoBase(BaseModel):
    nome: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    tipo: TipoDispositivo
    localizacao: Optional[str] = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_100)

    @field_validator("tipo", mode="before")
    @classmethod
    def validar_tipo(cls, v):
        if isinstance(v, TipoDispositivo):
            return v.value
        return v


class DispositivoCreate(DispositivoBase):
    pass

class DispositivoResponse(DispositivoBase):
    id: int

    class Config:
        from_attributes = True

class DispositivoUpdate(BaseModel):
    id: int
    nome: Optional[str] = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    localizacao: Optional[str] = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_100)
    tipo: Optional[TipoDispositivo] = None

    class Config:
        from_attributes = True
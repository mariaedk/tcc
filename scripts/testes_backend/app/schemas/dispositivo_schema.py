"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, Field
from app.models.enums import TipoDispositivo
import app.length_constants as length_constants

class DispositivoBase(BaseModel):
    nome: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    tipo: TipoDispositivo
    localizacao: str | None = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_100)

class DispositivoCreate(DispositivoBase):
    pass

class DispositivoResponse(DispositivoBase):
    id: int

    class Config:
        from_attributes = True

class DispositivoUpdate(BaseModel):
    id: int | None = None
    nome: str | None = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    localizacao: str | None = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_100)
    tipo: TipoDispositivo | None = None
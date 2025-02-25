"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel
from app.schemas.enums_schema import TipoDispositivo

class DispositivoBase(BaseModel):
    nome: str
    tipo: TipoDispositivo
    localizacao: str | None = None

class DispositivoCreate(DispositivoBase):
    pass

class DispositivoResponse(DispositivoBase):
    id: int

    class Config:
        orm_mode = True
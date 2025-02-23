"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel
from app.dtos.enums_dto import TipoDispositivo

class DispositivoDTO(BaseModel):
    nome: str
    tipo: TipoDispositivo
    localizacao: str | None = None

    class Config:
        orm_mode = True

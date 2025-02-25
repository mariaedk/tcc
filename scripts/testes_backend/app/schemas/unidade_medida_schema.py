"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel

class UnidadeMedidaBase(BaseModel):
    denominacao: str
    sigla: str

class UnidadeMedidaCreate(UnidadeMedidaBase):
    pass

class UnidadeMedidaResponse(UnidadeMedidaBase):
    id: int

    class Config:
        orm_mode = True

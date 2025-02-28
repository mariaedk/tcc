"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, Field
import app.length_constants as length_constants

class UnidadeMedidaBase(BaseModel):
    denominacao: str
    sigla: str

class UnidadeMedidaCreate(UnidadeMedidaBase):
    pass

class UnidadeMedidaResponse(UnidadeMedidaBase):
    id: int

    class Config:
        from_attributes = True

class UnidadeMedidaUpdate(BaseModel):
    id: int | None = None
    denominacao: str | None = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    sigla: str | None = Field(default=None, min_length=length_constants.SIZE_1, max_length=length_constants.SIZE_10)

"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel

class UnidadeMedidaDTO(BaseModel):
    id: int
    denominacao: str
    sigla: str

    class Config:
        orm_mode = True

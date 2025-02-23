"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel
from app.dtos.enums_dto import TipoUsuario

class UsuarioDTO(BaseModel):
    nome: str
    username: str
    email: str
    senha: str
    tipo: TipoUsuario

    class Config:
        orm_mode = True

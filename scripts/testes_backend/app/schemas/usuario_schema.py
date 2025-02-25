"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel
from app.schemas.enums_schema import TipoUsuario

class UsuarioBase(BaseModel):
    nome: str
    username: str
    email: str
    tipo: TipoUsuario

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        orm_mode = True

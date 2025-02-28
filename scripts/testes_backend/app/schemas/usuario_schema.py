"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, EmailStr, Field
from app.schemas.enums_schema import TipoUsuario
import app.length_constants as length_constants

class UsuarioBase(BaseModel):
    nome: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    username: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_100)
    email: EmailStr = Field(max_length=length_constants.SIZE_255)
    tipo: TipoUsuario

class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_10)

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    id: int | None = None
    nome: str | None = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    username: str | None = Field(default=None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_100)
    email: EmailStr | None = Field(default=None, max_length=length_constants.SIZE_255)
    tipo: TipoUsuario | None = None

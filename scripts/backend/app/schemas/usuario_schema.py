"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from app.models.enums import TipoUsuario
import app.length_constants as length_constants
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    username: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_100)
    email: EmailStr = Field(max_length=length_constants.SIZE_255)
    tipo: TipoUsuario

    @field_validator("tipo", mode="before")
    @classmethod
    def validar_tipo(cls, v):
        if isinstance(v, TipoUsuario):
            return v.value
        return v

class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_10)

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    id: int
    nome: Optional[str] = Field(None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_255)
    username: Optional[str] = Field(None, min_length=length_constants.SIZE_3, max_length=length_constants.SIZE_100)
    email: Optional[EmailStr] = Field(None, max_length=length_constants.SIZE_255)
    tipo: Optional[TipoUsuario] = None

    class Config:
        from_attributes = True


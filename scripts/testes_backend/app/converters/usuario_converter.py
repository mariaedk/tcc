"""
@author maria
date: 2025-02-23
"""

from app.models.usuario_model import Usuario
from app.dtos.usuario_dto import UsuarioDTO
from app.models.enums import TipoUsuario

def dto_to_model(dto: UsuarioDTO) -> Usuario:
    return Usuario(nome=dto.nome, username=dto.username, email=dto.email, senha=dto.senha, tipo=TipoUsuario[dto.tipo].value)

def model_to_dto(usuario: Usuario) -> UsuarioDTO:
    return UsuarioDTO(nome=usuario.nome, username=usuario.username, email=usuario.email, senha=usuario.senha, tipo=usuario.tipo.name)

"""
@author maria
date: 2025-02-23
"""

from app.models.dispositivo_model import Dispositivo
from app.dtos.dispositivo_dto import DispositivoDTO
from app.models.enums import TipoDispositivo

def model_to_dto(dto : DispositivoDTO) -> Dispositivo:
    return Dispositivo(nome=dto.nome, tipo=TipoDispositivo[dto.tipo].value, localizacao=dto.localizacao)

def dto_to_model(model : Dispositivo) -> DispositivoDTO:
    return DispositivoDTO(nome=model.nome, tipo=model.tipo.name, localizacao=model.localizacao)

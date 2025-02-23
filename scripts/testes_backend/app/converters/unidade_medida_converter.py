"""
@author maria
date: 2025-02-23
"""

from app.models.unidade_medida_model import UnidadeMedida
from app.dtos.unidade_medida_dto import UnidadeMedidaDTO

def model_to_dto(dto : UnidadeMedidaDTO) -> UnidadeMedida:
    return UnidadeMedida(denominacao=dto.denominacao, sigla=dto.sigla)

def dto_to_model(model : UnidadeMedida) -> UnidadeMedidaDTO:
    return UnidadeMedidaDTO(denominacao=model.denominacao, sigla=model.sigla)

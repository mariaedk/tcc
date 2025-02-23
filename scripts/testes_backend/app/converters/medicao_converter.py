"""
@author maria
date: 2025-02-23
"""

from app.models.medicao_model import Medicao
from app.dtos.medicao_dto import MedicaoDTO

def dto_to_model(dto: MedicaoDTO) -> Medicao:
    return Medicao(sensor_id=dto.sensor_id, unidade_id=dto.unidade_id, valor=dto.valor, data_hora=dto.data_hora)

def model_to_dto(model: Medicao) -> MedicaoDTO:
    return MedicaoDTO(sensor_id=model.sensor_id, unidade_id=model.unidade_id, valor=model.valor, data_hora=model.data_hora)


"""
@author maria
date: 2025-02-23
"""

from app.models.sensor_model import Sensor
from app.dtos.sensor_dto import SensorDTO
from app.models.enums import TipoSensor

def model_to_dto(dto : SensorDTO) -> Sensor:
    return Sensor(nome=dto.nome, tipo=TipoSensor[dto.tipo].value, dispositivo_id=dto.dispositivo_id)

def dto_to_model(model : Sensor) -> SensorDTO:
    return SensorDTO(nome=model.nome, tipo=model.tipo.name, dispositivo_id=model.dispositivo_id)

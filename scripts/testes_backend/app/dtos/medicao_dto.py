"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel
from datetime import datetime

class MedicaoDTO(BaseModel):
    id: int
    sensor_id: int
    unidade_id: int
    valor: float
    data_hora: datetime

    class Config:
        orm_mode = True

"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, Field
from datetime import datetime

class MedicaoBase(BaseModel):
    sensor_id: int
    unidade_id: int
    valor: float

class MedicaoCreate(MedicaoBase):
    pass

class MedicaoResponse(MedicaoBase):
    id: int
    data_hora: datetime

    class Config:
        from_attributes = True

"""
@author maria
date: 2025-02-23
"""

from pydantic import BaseModel, Field
from datetime import datetime

class MedicaoBase(BaseModel):
    sensor_id: int
    unidade_id: int
    valor: float = Field(default=None)

class MedicaoCreate(MedicaoBase):
    pass

class MedicaoResponse(MedicaoBase):
    id: int
    data_hora: datetime

    class Config:
        from_attributes = True

class MedicaoUpdate(BaseModel):
    id: int | None = None
    sensor_id: int | None = None
    unidade_id: int | None = None
    valor: float | None = None

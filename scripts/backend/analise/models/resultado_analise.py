"""
@author maria
date: 2025-04-21
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DadoAnalisado(BaseModel):
    data: datetime
    valor: float
    is_anomalia: bool

class ResultadoAnaliseSchema(BaseModel):
    total_medicoes: int
    anomalias: int
    mensagem: str
    dados: List[DadoAnalisado]
    ultimo_valor: float
    maximo: float
    unidade: str
    minimo: float
    dados_insuficientes: bool
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None

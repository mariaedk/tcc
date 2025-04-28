"""
@author maria
date: 2025-04-21
"""
from pydantic import BaseModel

class ResultadoAnaliseSchema(BaseModel):
    total_medicoes: int
    anomalias: int
    mensagem: str
    dados: list
    ultimo_valor: float
    maximo: float
    minimo: float
    data_inicio: str
    data_fim: str


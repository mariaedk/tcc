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

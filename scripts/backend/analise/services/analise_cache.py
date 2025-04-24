"""
@author maria
date: 2025-04-22
"""
from datetime import datetime, timedelta

class AnaliseCache:
    def __init__(self):
        self._cache = {}

    def salvar(self, sensor_codigo: int, resultado: dict):
        self._cache[sensor_codigo] = {
            "dados": resultado,
            "expira_em": datetime.utcnow() + timedelta(hours=1)
        }

    def obter(self, sensor_codigo: int):
        dados = self._cache.get(sensor_codigo)
        if dados and dados["expira_em"] > datetime.utcnow():
            return dados["dados"]
        return None

"""
@author maria
date: 2025-04-22
"""
from analise.services.analise_nivel import AnaliseNivel
from datetime import datetime, timezone, timedelta

UTC = timezone.utc

class AnaliseCache:
    def __init__(self):
        self._cache = {}

    def salvar(self, sensor_codigo: int, resultado: dict):
        self._cache[sensor_codigo] = {
            "dados": resultado,
            "expira_em": datetime.now(UTC) + timedelta(hours=1)
        }

    def obter(self, sensor_codigo: int):
        dados = self._cache.get(sensor_codigo)
        if dados and dados["expira_em"] > datetime.now(UTC):
            return dados["dados"]
        return None

class AnaliseNivelService:
    def __init__(self, dias: int = 7):
        self.dias = dias
        self.cache = AnaliseCache()
        self.analise = AnaliseNivel(dias)

    def analisar(self, medicoes: list[dict], sensor_codigo: int) -> dict:
        cacheado = self.cache.obter(sensor_codigo)
        if cacheado:
            return cacheado

        resultado = self.analise.analisar(medicoes)
        self.cache.salvar(sensor_codigo, resultado)
        return resultado
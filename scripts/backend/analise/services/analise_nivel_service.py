from analise.services.analise_nivel import AnaliseNivel
from datetime import datetime, timezone, timedelta
from app.models.enums import TipoMedicao
from app.schemas.medicao_schema import MedicaoHistoricoSchema
import hashlib

UTC = timezone.utc

class AnaliseCache:
    def __init__(self):
        self._cache = {}

    @staticmethod
    def _gerar_chave(sensor_codigo: int, tipo: TipoMedicao, **filtros) -> str:
        base = f"{sensor_codigo}_{tipo}_" + "_".join(
            f"{k}:{v}" for k, v in sorted(filtros.items()) if v is not None
        )
        return hashlib.md5(base.encode()).hexdigest()

    def salvar(self, sensor_codigo: int, tipo: TipoMedicao, resultado: dict, **filtros):
        chave = self._gerar_chave(sensor_codigo, tipo, **filtros)
        self._cache[chave] = {
            "dados": resultado,
            "expira_em": datetime.now(UTC) + timedelta(hours=1)
        }

    def obter(self, sensor_codigo: int, tipo: TipoMedicao, **filtros):
        chave = self._gerar_chave(sensor_codigo, tipo, **filtros)
        dados = self._cache.get(chave)
        if dados and dados["expira_em"] > datetime.now(UTC):
            return dados["dados"]
        return None

class AnaliseNivelService:
    def __init__(self):
        self.cache = AnaliseCache()
        self.analise = AnaliseNivel()

    def analisar(
        self,
        medicoes: list[MedicaoHistoricoSchema],
        sensor_codigo: int,
        tipo: TipoMedicao,
        data: datetime = None,
        data_inicio: datetime = None,
        data_fim: datetime = None,
        dias: int = None
    ) -> dict:
        cacheado = self.cache.obter(
            sensor_codigo,
            tipo,
            data=data,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dias=dias
        )

        if cacheado:
            return cacheado

        resultado = self.analise.analisar(medicoes)
        self.cache.salvar(
            sensor_codigo,
            tipo,
            resultado,
            data=data,
            data_inicio=data_inicio,
            data_fim=data_fim,
            dias=dias
        )

        return resultado
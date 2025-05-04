from typing import Any

from sklearn.ensemble import IsolationForest
import pandas as pd
from analise.models.resultado_analise import ResultadoAnaliseSchema
from app.schemas.medicao_schema import MedicaoHistoricoSchema

class AnaliseNivel:

    def __init__(self):
        self.modelo = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)

    def analisar(self, medicoes: list[MedicaoHistoricoSchema]):
        if not medicoes:
            return {"status": "sem dados suficientes"}

        dados_dict = [m.model_dump() for m in medicoes]
        df = pd.DataFrame(dados_dict)
        df.sort_values('data', inplace=True)

        if len(df) < 5:
            return {
                "total_medicoes": 0,
                "anomalias": 0,
                "dados_insuficientes": True,
                "mensagem": "Dados insuficientes",
                "dados": [],
                "ultimo_valor": 0,
                "maximo": 0,
                "minimo": 0
            }

        valores = df['valor'].values.reshape(-1, 1)
        self.modelo.fit(valores)
        df['anomaly'] = self.modelo.predict(valores)
        df['is_anomalia'] = df['anomaly'] == -1

        dados_completos = df[['data', 'valor', 'is_anomalia']].to_dict(orient='records')
        qtd_anomalias = df['is_anomalia'].sum()

        if qtd_anomalias == 0:
            insight = "Nível estável."
        elif qtd_anomalias <= 2:
            insight = "Pequenas variações detectadas no nível de água."
        else:
            insight = f"Nível apresentou {qtd_anomalias} comportamentos anômalos."

        resp = {
            "total_medicoes": len(df),
            "anomalias": qtd_anomalias,
            "mensagem": insight,
            "dados": dados_completos,
            "dados_insuficientes": False,
            "ultimo_valor": float(df['valor'].iloc[-1]),
            "maximo": float(df['valor'].max()),
            "minimo": float(df['valor'].min()),
            "data_inicio": df['data'].min(),
            "data_fim": df['data'].max(),
        }

        return ResultadoAnaliseSchema(**resp)

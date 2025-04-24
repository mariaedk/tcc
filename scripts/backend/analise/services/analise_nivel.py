"""
@author maria
date: 2025-04-21
"""
from sklearn.ensemble import IsolationForest
import pandas as pd
from analise.models.resultado_analise import ResultadoAnaliseSchema

class AnaliseNivel:

    def __init__(self, dias=7):
        self.dias = dias
        self.modelo = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)

    def analisar(self, medicoes: list[dict]) -> dict:

        if not medicoes:
            return {"status": "sem dados suficientes"}

        # transforma a data em datetime.
        df = pd.DataFrame(medicoes)
        df['data'] = pd.to_datetime(df['data'])

        # ordena os dados pra deixar em ordem cronologica
        df.sort_values('data', inplace=True)

        if len(df) < 5:
            return {"status": "poucos dados para análise"}

        # transforma o vetor 1d em matriz (2d)
        valores = df['media_valor'].values.reshape(-1, 1)

        # treina o modelo.
        self.modelo.fit(valores)
        df['anomaly'] = self.modelo.predict(valores)

        # conta a quantidade de anomalias.
        # cria uma série bool com colunas true/false. se anomaly for -1 retorna true
        # IsolationForest classifica 1 sendo normal e -1 anomalo.
        # sum conta todos os true.
        qtd_anomalias = (df['anomaly'] == -1).sum()

        if qtd_anomalias == 0:
            insight = "Nível estável nos últimos dias."
        elif qtd_anomalias <= 2:
            insight = "Pequenas variações detectadas no nível de água."
        else:
            insight = f"Nível apresentou {qtd_anomalias} comportamentos anômalos."

        resp = {
            "total_medicoes": len(df),
            "anomalias": qtd_anomalias,
            "mensagem": insight
        }

        return ResultadoAnaliseSchema(**resp)
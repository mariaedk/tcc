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

        # CONVERTE os medicoes para dict
        dados_dict = [m.model_dump() for m in medicoes]
        df = pd.DataFrame(dados_dict)

        # ordena os dados pela data
        df.sort_values('data', inplace=True)

        if len(df) < 5:
            return {"status": "poucos dados para análise"}

        # transforma o vetor 1d em matriz (2d)
        valores = df['valor'].values.reshape(-1, 1)

        # treina o modelo
        self.modelo.fit(valores)
        df['anomaly'] = self.modelo.predict(valores)
        df['is_anomalia'] = df['anomaly'] == -1

        dados_completos = df[['data', 'valor', 'is_anomalia']].to_dict(orient='records')

        qtd_anomalias = df['is_anomalia'].sum()

        if qtd_anomalias == 0:
            insight = f"Nível estável nos últimos {self.dias} dias."
        elif qtd_anomalias <= 2:
            insight = f"Pequenas variações detectadas no nível de água nos últimos {self.dias} dias."
        else:
            insight = f"Nível apresentou {qtd_anomalias} comportamentos anômalos nos últimos {self.dias} dias."

        resp = {
            "total_medicoes": len(df),
            "anomalias": qtd_anomalias,
            "mensagem": insight,
            "dados": dados_completos,
            "ultimo_valor": float(df['valor'].iloc[-1]),
            "maximo": float(df['valor'].max()),
            "minimo": float(df['valor'].min()),
            "data_inicio": df['data'].min().strftime('%d/%m/%Y'),
            "data_fim": df['data'].max().strftime('%d/%m/%Y')
        }

        return ResultadoAnaliseSchema(**resp)

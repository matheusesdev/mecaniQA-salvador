"""
MecaniQA - Encontro (12/08/2026): Decomposicao da Serie Temporal
Piloto: Juan Pablo Barros Carvalho | Copiloto: Albert Santos Soares
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# Garante que o caminho funcione independente de onde o script for executado
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(PASTA_ATUAL, "mecaniqa_dataset.csv")
caminho_grafico = os.path.join(PASTA_ATUAL, "decomposicao_trocas_oleo.png")

# 1) Preparar o dataset (index = data, ordenado cronologicamente)
df = pd.read_csv(caminho_csv)
df["Data"] = pd.to_datetime(df["Data"])
df = df.set_index("Data").sort_index()

# Serie alvo: trocas de oleo por dia
# Observacao: a base tem 6 valores ausentes em Trocas_Oleo.
# seasonal_decompose nao aceita NaN, entao interpolamos linearmente
# antes de decompor (mantendo o indice diario continuo).
serie = df["Trocas_Oleo"].interpolate(method="linear")

# 2) Decomposicao aditiva, period=7 (ciclo semanal, dados diarios)
resultado = seasonal_decompose(serie, model="additive", period=7)

# 3) Plot com os 4 graficos empilhados
fig = resultado.plot()
fig.set_size_inches(10, 8)
fig.suptitle("Decomposicao da Serie Temporal - Trocas de Oleo (MecaniQA)", y=1.02)
plt.tight_layout()
plt.savefig(caminho_grafico, dpi=150, bbox_inches="tight")
plt.show()

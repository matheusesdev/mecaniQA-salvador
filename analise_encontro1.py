"""
MecaniQA - Encontro 1: Exploracao de Estruturas de Dados Temporais
Piloto: Juan Pablo Barros Carvalho
"""
import pandas as pd
import os

# Garante que o caminho funcione independente de onde o script for executado
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
caminho_csv = os.path.join(PASTA_ATUAL, "mecaniqa_dataset.csv")

# 1) Importacao do dataset e indexacao temporal
# (o time decidiu usar pd.read_csv + pd.to_datetime + set_index)
df = pd.read_csv(caminho_csv)
df["Data"] = pd.to_datetime(df["Data"])
df = df.set_index("Data")
df = df.sort_index()

# 2) Inspecao inicial
print(df.head())
print(df.info())

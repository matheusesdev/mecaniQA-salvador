"""Validacao temporal dos baselines com previsoes de um dia a frente."""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
)
from sklearn.model_selection import TimeSeriesSplit


def calcular_metricas(real, previsto):
    """Recebe pares validos; zeros sao excluidos apenas do MAPE."""
    real = np.asarray(real, dtype=float)
    previsto = np.asarray(previsto, dtype=float)
    if real.ndim != 1 or real.shape != previsto.shape or not real.size:
        raise ValueError("Informe vetores de mesmo tamanho, nao vazios.")
    if not np.isfinite(real).all() or not np.isfinite(previsto).all():
        raise ValueError("As metricas exigem pares finitos.")
    nao_zero = real != 0
    return {
        "MAE": mean_absolute_error(real, previsto),
        "RMSE": np.sqrt(mean_squared_error(real, previsto)),
        "MAPE (%)": (
            100 * mean_absolute_percentage_error(real[nao_zero], previsto[nao_zero])
            if nao_zero.any() else float("nan")
        ),
        "Dias avaliados": len(real),
        "Dias MAPE": int(nao_zero.sum()),
    }


def avaliar_baselines(serie, n_splits=5, janela=7):
    """Retorna metricas por fold, resumo agregado e previsoes de teste."""
    if not isinstance(serie.index, pd.DatetimeIndex) or serie.index.hasnans:
        raise ValueError("A serie deve ter um DatetimeIndex sem datas ausentes.")
    if not isinstance(janela, int) or janela < 1:
        raise ValueError("A janela deve ser um inteiro positivo.")
    serie = pd.to_numeric(serie, errors="raise").sort_index()
    if np.isinf(serie).any() or (serie.dropna() < 0).any():
        raise ValueError("A demanda deve ser nao negativa e sem infinitos.")
    serie = serie.resample("D").sum(min_count=1)
    media = f"Media movel ({janela} dias)"
    modelos = ["Naive", media]
    registros, testes = [], []
    for fold, (treino, teste) in enumerate(
        TimeSeriesSplit(n_splits=n_splits).split(serie), start=1
    ):
        # O prefixo inclui observacoes do teste, disponiveis apenas no dia seguinte.
        passado = serie.iloc[:teste[-1] + 1].ffill().shift(1)
        previsoes = pd.DataFrame({
            "Real": serie.iloc[teste],
            "Naive": passado.iloc[teste],
            media: passado.rolling(janela).mean().iloc[teste],
        })
        validos = previsoes.dropna()
        if validos.empty:
            raise ValueError(f"Fold {fold} sem pares validos para os dois modelos.")
        for modelo in modelos:
            registros.append({
                "Fold": fold,
                "Modelo": modelo,
                "Inicio treino": serie.index[treino[0]],
                "Fim treino": serie.index[treino[-1]],
                "Inicio teste": serie.index[teste[0]],
                "Fim teste": serie.index[teste[-1]],
                "Dias excluidos": len(previsoes) - len(validos),
                **calcular_metricas(validos["Real"], validos[modelo]),
            })
        previsoes["Fold"] = fold
        testes.append(previsoes)
    previsoes = pd.concat(testes)
    validos = previsoes.dropna(subset=["Real", *modelos])
    resumo = pd.DataFrame([
        {"Modelo": modelo, **calcular_metricas(validos["Real"], validos[modelo])}
        for modelo in modelos
    ]).set_index("Modelo")
    return pd.DataFrame(registros), resumo, previsoes


def imprimir_boletim(metricas_por_fold, resumo):
    print("Validacao temporal: previsao diaria de um passo a frente")
    print(metricas_por_fold.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print("\nBoletim agregado - MAE e RMSE em trocas de oleo por dia")
    for modelo, metricas in resumo.iterrows():
        mape = metricas["MAPE (%)"]
        percentual = f"{mape:.2f}%" if pd.notna(mape) else "indefinido (sem reais nao zero)"
        print(modelo)
        print(
            f"Resultados do Baseline - MAE: {metricas['MAE']:.4f}, "
            f"RMSE: {metricas['RMSE']:.4f}, MAPE: {percentual}"
        )
    print(f"Melhor baseline pelo menor MAE: {resumo['MAE'].idxmin()}")


def carregar_serie(caminho=None):
    """Usa o Excel versionado por padrao; tambem aceita o CSV da equipe."""
    caminho = Path(caminho) if caminho else Path(__file__).parent / "data/mecaniqa_dataset.xlsx"
    dados = pd.read_csv(caminho) if caminho.suffix.lower() == ".csv" else pd.read_excel(caminho)
    dados["Data"] = pd.to_datetime(dados["Data"], errors="raise")
    return dados.set_index("Data")["Trocas_Oleo"].sort_index()


if __name__ == "__main__":
    metricas_por_fold, resumo_baselines, previsoes_validacao = avaliar_baselines(carregar_serie())
    imprimir_boletim(metricas_por_fold, resumo_baselines)

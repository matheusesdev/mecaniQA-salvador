"""Tratamento e baselines usados na entrega da OAT 1."""

from __future__ import annotations

import pandas as pd


def _limites_iqr(serie: pd.Series) -> tuple[float, float]:
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    intervalo = q3 - q1
    return q1 - 1.5 * intervalo, q3 + 1.5 * intervalo


def tratar_dados_mecaniqa(dados: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Limpa a linha do tempo sem usar informação posterior nos baselines.

    Datas ausentes e valores inválidos são marcados como ausentes e interpolados
    apenas nesta etapa de preparação. O outlier é detectado pela regra do IQR.
    """
    colunas = {"Data", "Trocas_Oleo", "Manutencao_Motor"}
    faltantes = colunas.difference(dados.columns)
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(faltantes)}")

    limpos = dados.loc[:, ["Data", "Trocas_Oleo", "Manutencao_Motor"]].copy()
    limpos["Data"] = pd.to_datetime(limpos["Data"], errors="raise")
    limpos = limpos.sort_values("Data").set_index("Data").asfreq("D")

    relatorio = {
        "ausentes_trocas_oleo": int(limpos["Trocas_Oleo"].isna().sum()),
        "ausentes_manutencao_motor": int(limpos["Manutencao_Motor"].isna().sum()),
    }

    limite_inferior, limite_superior = _limites_iqr(limpos["Trocas_Oleo"].dropna())
    mascara_outlier = ~limpos["Trocas_Oleo"].between(
        limite_inferior, limite_superior, inclusive="both"
    ) & limpos["Trocas_Oleo"].notna()
    mascara_negativos = limpos["Manutencao_Motor"].lt(0)

    relatorio["outliers_trocas_oleo"] = int(mascara_outlier.sum())
    relatorio["negativos_manutencao_motor"] = int(mascara_negativos.sum())

    limpos.loc[mascara_outlier, "Trocas_Oleo"] = pd.NA
    limpos.loc[mascara_negativos, "Manutencao_Motor"] = pd.NA
    limpos = limpos.interpolate(method="time", limit_direction="both")

    return limpos, relatorio


def criar_baselines(serie: pd.Series) -> pd.DataFrame:
    """Cria os três baselines da OAT 1 usando somente valores anteriores a t."""
    passado = serie.shift(1)
    return pd.DataFrame(
        {
            "Real": serie,
            "Naive": passado,
            "Média móvel (7 dias)": passado.rolling(7, min_periods=7).mean(),
            "Média móvel (30 dias)": passado.rolling(30, min_periods=30).mean(),
        }
    )

"""Configuração reproduzível das buscas de hiperparâmetros da OAT 3."""

from __future__ import annotations

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, TimeSeriesSplit


def descrever_variacao_percentual(inicial: float, final: float) -> str:
    """Traduz a variação do erro sem chamar uma piora de redução."""
    if inicial <= 0:
        raise ValueError("O erro inicial deve ser positivo")
    variacao = 100 * (final - inicial) / inicial
    verbo = "reduziu" if variacao < 0 else "aumentou"
    return f"{verbo} em {abs(variacao):.2f}%"


def criar_buscas_random_forest(
    *, random_state: int = 42, n_iter: int = 10
) -> tuple[GridSearchCV, RandomizedSearchCV]:
    """Cria Grid e Random Search comparáveis e protegidos temporalmente."""
    if n_iter < 1:
        raise ValueError("n_iter deve ser positivo")

    espaco = {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 5, 10],
        "min_samples_split": [2, 5, 10],
    }
    modelo = RandomForestRegressor(random_state=random_state)
    scoring = "neg_mean_absolute_percentage_error"

    grid = GridSearchCV(
        estimator=modelo,
        param_grid=espaco,
        scoring=scoring,
        cv=TimeSeriesSplit(n_splits=5),
        n_jobs=1,
        refit=True,
    )
    random = RandomizedSearchCV(
        estimator=modelo,
        param_distributions=espaco,
        n_iter=n_iter,
        scoring=scoring,
        cv=TimeSeriesSplit(n_splits=5),
        random_state=random_state,
        n_jobs=1,
        refit=True,
    )
    return grid, random

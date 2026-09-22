# 🔧 MecâniQA Automotive Tech — OAT 2

Projeto de Ciência de Dados e Séries Temporais do Programa de Trainee 2026.2. A entrega consolidada está em `notebooks/oat2_pipeline_preditivo.ipynb` e analisa a série diária `Trocas_Oleo`.

## Entregas práticas

O notebook contém:

- funções para os baselines Naive e média móvel de 7 dias;
- gráfico com histórico real e os dois baselines;
- proteção contra vazamento com `shift(1)`;
- validação cronológica com `TimeSeriesSplit`;
- MAE, RMSE e MAPE para os dois baselines no formato pedido;
- features `lag_1`, `lag_7`, `lag_30`, `rolling_7` e `rolling_30`;
- tratamento dos NaNs iniciais e conferência com `df.head(15)`;
- pipeline Ridge com imputação, padronização e ajuste temporal de `alpha`.

## Decisões da equipe

### Baselines sem vazamento — 02/09

- Aplicar `shift(1)` antes da previsão ou janela móvel. A previsão de `t` usa no máximo dados de `t-1`.
- Implementar funções simples e independentes, sem interfaces ou classes abstratas.

### Métricas e validação — 09/09

- MAE representa o erro absoluto médio na unidade da demanda. RMSE penaliza mais os erros grandes e evidencia melhor os picos fora da curva.
- `TimeSeriesSplit` mantém treino antes de teste. K-Fold pode treinar com datas posteriores às avaliadas.

Nos resultados medidos pela equipe, o Naive teve o menor MAE, aproximadamente 6,65 trocas por dia, e foi escolhido como referência principal. A média móvel de 7 dias teve RMSE menor. O MAPE exclui somente os valores reais iguais a zero.

### Features temporais — 16/09

- `lag_1` captura o curto prazo, `lag_7` o ciclo semanal e `lag_30` uma referência mensal.
- As linhas iniciais de aquecimento são removidas depois da criação das features. Nenhum lag é preenchido com dados futuros.

## Como executar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
jupyter notebook
```

Execute todas as células do notebook na ordem. O caminho do dataset funciona quando o Jupyter é iniciado pela raiz ou pela pasta `notebooks`.

O boletim segue o formato exigido:

```text
Resultados do Baseline - MAE: X, RMSE: Y, MAPE: Z%
```

## Estrutura principal

```text
mecaniQA-salvador/
├── data/mecaniqa_dataset.xlsx
├── notebooks/oat1_compreensao_baseline.ipynb
├── notebooks/oat2_pipeline_preditivo.ipynb
├── tests/test_oat2_delivery.ps1
├── README.md
└── requirements.txt
```

## Entrega

Os ajustes foram desenvolvidos na branch `feat/consolidacao-oat2`. Depois da revisão da equipe, a branch deve ser integrada à `main`, conforme solicitado pelo professor.

# 🔧 MecâniQA Automotive Tech — OAT 2

Projeto de Ciência de Dados e Séries Temporais do Programa de Trainee 2026.2. A entrega consolidada está em `notebooks/oat2_pipeline_preditivo.ipynb` e analisa a série diária `Trocas_Oleo`.

## OAT 1 — Compreensão, decomposição e pipeline

A OAT 1 utiliza `data/mecaniqa_dataset.xlsx` e tem como notebooks oficiais:

- `notebooks/oat1_compreensao_baseline.ipynb`, para inspeção, decomposição e registro dos baselines;
- `notebooks/oat1_pipeline_preditivo.ipynb`, para o pipeline preditivo.

A série principal é `Trocas_Oleo`. A OAT 1 preserva o dataset original e limpa uma cópia de trabalho: interpola ausentes, identifica outliers pela regra do IQR e substitui os valores inválidos por interpolação temporal. A análise descritiva usa decomposição aditiva com periodicidade de sete dias. O pipeline combina `SimpleImputer`, `StandardScaler` e regressão `Ridge`, com seleção de `alpha` por `TimeSeriesSplit`. A divisão é cronológica: 80% dos registros preparados para treino e os 20% finais para teste, sem embaralhamento.

Para executar, instale as dependências com `python -m pip install -r requirements.txt`, inicie o Jupyter pela raiz do projeto e execute todas as células dos dois notebooks na ordem.

### Escopo efetivamente implementado na OAT 1

A OAT 1 trata valores ausentes, o valor extremo de 150 em `Trocas_Oleo` e valores negativos em `Manutencao_Motor` sem modificar o arquivo de origem. Os baselines utilizam o valor anterior e médias móveis de 7 e 30 dias, sempre com `shift(1)` para impedir vazamento do valor previsto. A validação consolidada e oficial dos baselines permanece na OAT 2.

## OAT 2 — Baselines, validação temporal e features

O notebook oficial da entrega é `notebooks/oat2_pipeline_preditivo.ipynb`.

### Entregas práticas

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

Na validação temporal dos baselines, o Naive obteve MAE 6,6463, RMSE 8,9185 e MAPE 32,64%; a média móvel de 7 dias obteve MAE 7,3558, RMSE 8,0881 e MAPE 37,22%. O Naive permanece como baseline principal pelo menor MAE, enquanto a média móvel apresentou o menor RMSE.

No teste cronológico final, o pipeline Ridge obteve MAE 4,106, RMSE 4,955 e R² 0,676, com `alpha` 10 selecionado por `TimeSeriesSplit`.

### Features temporais — 16/09

- `lag_1` captura o curto prazo, `lag_7` o ciclo semanal e `lag_30` uma referência mensal.
- `rolling_7` e `rolling_30` resumem janelas de 7 e 30 dias; ambas usam `shift(1)` antes de `rolling()`.
- As linhas iniciais de aquecimento são removidas depois da criação das features. Nenhum lag é preenchido com dados futuros.

## OAT 3 — Entregas consolidadas até 14/10

O notebook `notebooks/oat3_pipeline_preditivo.ipynb` registra as decisões e entregas dos encontros de 30/09, 07/10 e 14/10. Conforme o caderno da equipe, os modelos iniciais são `DecisionTreeRegressor` e `RandomForestRegressor`, treinados em uma divisão cronológica 80/20 e comparados com o baseline Naive por RMSE e MAPE.

O notebook reutiliza a limpeza validada da OAT 1 e não modifica o dataset original. O Random Forest inicial venceu a comparação, com RMSE 3,5976 e MAPE 12,02%. A sintonia utiliza o mesmo Random Forest com `TimeSeriesSplit`: o Grid Search examina todas as 27 combinações registradas, enquanto o Random Search limita a busca a 10 combinações. Na execução versionada, o Grid Search encontrou `max_depth=None`, `min_samples_split=5` e `n_estimators=300`; o Random Search encontrou `max_depth=10`, `min_samples_split=5` e `n_estimators=100`.

O notebook mede os tempos em cada execução e registra o trade-off sem presumir ganho. Na execução versionada, o Grid Search reduziu o MAPE em 1,59%; o Random Search reduziu o MAPE em 1,24% e economizou 68,70% do tempo do Grid, ficando apenas 0,04 ponto percentual acima dele. A entrega de 21/10 não faz parte desta consolidação.

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

```bash
mecaniQA-salvador/
├── data/mecaniqa_dataset.xlsx
├── notebooks/oat1_compreensao_baseline.ipynb
├── notebooks/oat1_pipeline_preditivo.ipynb
├── notebooks/oat2_pipeline_preditivo.ipynb
├── tests/test_oat2_delivery.ps1
├── README.md
└── requirements.txt
```

## Entrega

A entrega consolidada da OAT 2 foi revisada e integrada à branch `main`.

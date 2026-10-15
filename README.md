# MecâniQA Automotive Tech — Modelos de Aprendizado de Máquina

Projeto desenvolvido pela equipe MecaniQA Salvador na disciplina **Modelos de Aprendizado de Máquina**. O trabalho utiliza como contexto a MecâniQA Automotive Tech, empresa fictícia de Feira de Santana que fornece soluções de gestão para lojas de autopeças, autocentros e oficinas mecânicas.

O problema de negócio é a dificuldade de prever a procura por serviços de manutenção preventiva. Oscilações diárias podem causar falta de peças, sobrecarga da equipe ou ociosidade dos mecânicos. Para apoiar o planejamento operacional, o projeto constrói e compara métodos de previsão para as séries diárias de trocas de óleo e manutenções de motor.

O desenvolvimento é incremental e organizado em OATs:

- **OAT 1 — Compreensão e baseline:** entendimento, qualidade e decomposição dos dados, primeiros baselines e pipeline preditivo;
- **OAT 2 — Baselines e métricas de avaliação:** prevenção de vazamento temporal, validação, métricas e criação de features;
- **OAT 3 — Tunando o modelo:** comparação de modelos clássicos e otimização de hiperparâmetros.

O dataset contém 731 registros diários, de 01/01/2024 a 31/12/2025, nas colunas `Data`, `Trocas_Oleo` e `Manutencao_Motor`. O arquivo original é preservado em `data/mecaniqa_dataset.xlsx`; os tratamentos são aplicados em cópias de trabalho.

## Membros da equipe

- Albert Santos Soares;
- Juan Pablo Barros Carvalho;
- Matheus Espírito Santo dos Santos;
- Rafael Pires Araújo;
- William Bichara de Souza.

Os nomes foram padronizados nesta apresentação geral. Nas sessões, os papéis e as marcações de ausência seguem os registros dos respectivos cadernos.

## Organização das sessões

O projeto segue uma dinâmica inspirada em Scrum. Em cada sessão, a equipe interpreta o desafio do caderno, discute as alternativas, registra as decisões, implementa o código, valida o resultado e prepara as evidências da entrega. Os papéis de Piloto, Copiloto, QA, Arquiteto/Documentador e Scrum Master/Apresentador são distribuídos entre os integrantes.

Este README distingue quatro elementos em cada encontro:

- **decisões da equipe:** abordagem registrada no caderno;
- **entrega solicitada:** evidência pedida pelo professor em “Entrega do encontro”;
- **implementação:** onde a decisão aparece no código versionado;
- **resultado:** saída reproduzível ou situação atual da entrega.

## Situação atual

| OAT | Período consolidado | Situação | Artefato principal |
|---|---|---|---|
| OAT 1 | 12/08 a 26/08, com correção documental em 15/10 | Concluída e alinhada ao slide entregue | `notebooks/oat1_compreensao_baseline.ipynb` e `notebooks/oat1_pipeline_preditivo.ipynb` |
| OAT 2 | 02/09 a 16/09 | Concluída | `notebooks/oat2_pipeline_preditivo.ipynb` |
| OAT 3 | 30/09 a 14/10 | Código consolidado até 14/10 | `notebooks/oat3_pipeline_preditivo.ipynb` |
| OAT 3 — fechamento | 21/10 | Não realizado neste momento | Slides ainda não criados |

## OAT 1 — Compreensão e baseline

### 12/08/2026 — 1ª sessão: compreensão e qualidade dos dados

- **Equipe da sessão:** Albert Santos Soares — Piloto; Juan Pablo Barros Carvalho — Copiloto; Matheus Espírito Santo dos Santos — QA; Rafael Pires Araújo — Arquiteto; William Bichara de Souza — Scrum Master.
- **Decisões da equipe:** interpretar `Data` como índice temporal, manter os registros em ordem cronológica e investigar valores ausentes, negativos e extremos antes da modelagem.
- **Entrega solicitada:** primeira versão do notebook com importação dos dados, `head()` e `info()`, versionada no repositório.
- **Implementação:** `notebooks/oat1_compreensao_baseline.ipynb` carrega o Excel, inspeciona a estrutura e apresenta o diagnóstico de qualidade. A limpeza reutilizável está em `oat1_processing.py` e atua sobre uma cópia, sem modificar o arquivo original.
- **Resultado:** foram identificados 6 valores ausentes em `Trocas_Oleo`, 3 em `Manutencao_Motor`, 1 valor extremo e 5 valores negativos. Após o tratamento, não permanecem ausentes; o maior valor de trocas de óleo é 53 e a manutenção mínima é 0.

### 12/08/2026 — 2ª sessão: tendência, sazonalidade e ruído

> O caderno registra a mesma data para as duas primeiras sessões. O registro foi mantido para não inventar uma cronologia diferente da documentação da equipe.

- **Equipe da sessão:** Juan Pablo Barros Carvalho — Piloto; Albert Santos Soares — Copiloto; Matheus Espírito Santo dos Santos — QA; Rafael Pires Araújo — Arquiteto; William Bichara de Souza — Scrum Master.
- **Decisões da equipe:** usar decomposição aditiva e período de 7 dias, coerente com a hipótese de comportamento semanal.
- **Entrega solicitada:** aplicar `seasonal_decompose` sobre uma série com `DatetimeIndex` e exibir observado, tendência, sazonalidade e resíduo.
- **Implementação:** o notebook de compreensão ordena os dados por data, cria o índice temporal e executa a decomposição aditiva com `period=7`.
- **Resultado:** a série pode ser examinada separando nível observado, tendência, componente semanal e ruído, servindo de base para os primeiros métodos de previsão.

### 26/08/2026 — 3ª sessão: pipeline preditivo

- **Equipe da sessão:** William Bichara de Souza — Piloto; Rafael Pires Araújo — Copiloto; Albert Santos Soares — QA; Juan Pablo Barros Carvalho — Arquiteto; Matheus Espírito Santo dos Santos — Scrum Master.
- **Decisões da equipe:** encapsular preparação e modelo em um `Pipeline`, ajustar transformadores somente com o treino e manter a divisão cronológica.
- **Entrega solicitada:** construir um pipeline com transformador e estimador e treiná-lo com uma chamada a `pipeline.fit(X_train, y_train)`.
- **Implementação:** `notebooks/oat1_pipeline_preditivo.ipynb` combina `SimpleImputer`, `StandardScaler` e regressão `Ridge`. O `alpha` é selecionado com `GridSearchCV` e `TimeSeriesSplit`, usando os primeiros 80% dos registros preparados para treino e os 20% finais para teste.
- **Resultado:** foi estabelecido um fluxo único e reproduzível para imputação, padronização, ajuste e previsão, sem embaralhar a série temporal.

### 15/10/2026 — Correção de alinhamento da OAT 1

- **Equipe da sessão:** não se aplica. Esta foi uma correção posterior de alinhamento, e não uma sessão registrada no caderno com nova distribuição de papéis.
- **Motivo:** fazer o código corresponder ao conteúdo já apresentado nos slides da OAT 1, sem alterar a apresentação entregue.
- **Implementação:** a limpeza passou a tratar ausentes, o valor extremo de `Trocas_Oleo` e valores negativos de `Manutencao_Motor`. Também foram consolidados os baselines Naive e médias móveis de 7 e 30 dias, todos com `shift(1)` para impedir o uso do valor que está sendo previsto.
- **Impacto controlado:** o dataset original permaneceu intacto. O tratamento compartilhado foi incorporado à OAT 3 e os resultados posteriores foram novamente validados.
- **Rastreabilidade:** correção registrada no commit `497458b` e integrada à `main`.

## OAT 2 — Baselines e métricas de avaliação

### 02/09/2026 — 1ª sessão: baselines sem vazamento temporal

- **Equipe da sessão:** Matheus Espírito Santo dos Santos — Piloto; Rafael Pires Araújo — Copiloto; Albert Santos Soares — QA; William Bichara de Souza **(AUSENTE)** — Arquiteto; Juan Pablo Barros Carvalho — Scrum Master.
- **Decisões da equipe:** aplicar `shift(1)` antes das previsões e janelas móveis, usar somente informações disponíveis até `t-1` e manter funções simples e independentes.
- **Entrega solicitada:** implementar `baseline_naive`, média móvel de 7 dias e gráfico comparando valores reais e previsões, com validação de QA contra vazamento.
- **Implementação:** `notebooks/oat2_pipeline_preditivo.ipynb` implementa os dois baselines e gera a comparação visual sobre a série `Trocas_Oleo`.
- **Resultado:** as previsões respeitam a ordem temporal; o valor real do instante previsto não entra no cálculo da própria previsão.

### 09/09/2026 — 2ª sessão: métricas e validação temporal

- **Equipe da sessão:** Juan Pablo Barros Carvalho — Piloto; Matheus Espírito Santo dos Santos — Copiloto; Rafael Pires Araújo **(AUSENTE)** — QA; William Bichara de Souza **(AUSENTE)** — Arquiteto; Albert Santos Soares **(AUSENTE)** — Scrum Master.
- **Decisões da equipe:** usar MAE para interpretar o erro médio na unidade da demanda, RMSE para penalizar erros maiores e `TimeSeriesSplit` no lugar de K-Fold aleatório. O MAPE desconsidera apenas observações cujo valor real é zero.
- **Entrega solicitada:** calcular MAE, RMSE e MAPE para os dois baselines, demonstrar a divisão temporal e registrar qual abordagem seria a referência.
- **Implementação:** o notebook avalia cada baseline em divisões temporais expansivas e imprime as métricas no formato pedido pelo professor.
- **Resultado:** o Naive obteve MAE 6,6463, RMSE 8,9185 e MAPE 32,64%; a média móvel de 7 dias obteve MAE 7,3558, RMSE 8,0881 e MAPE 37,22%. O Naive foi mantido como referência principal pelo menor MAE, enquanto a média móvel apresentou menor RMSE.

### 16/09/2026 — 3ª sessão: features temporais

- **Equipe da sessão:** Albert Santos Soares **(AUSENTE)** — Piloto; Juan Pablo Barros Carvalho — Copiloto; Matheus Espírito Santo dos Santos — QA; Rafael Pires Araújo — Arquiteto; William Bichara de Souza **(AUSENTE)** — Scrum Master.
- **Decisões da equipe:** criar `lag_1`, `lag_7` e `lag_30`, além de `rolling_7` e `rolling_30`; aplicar `shift(1)` antes das janelas e remover somente as linhas iniciais de aquecimento.
- **Entrega solicitada:** adicionar as features, tratar os NaNs gerados e comprovar o resultado com as primeiras linhas e a contagem de nulos.
- **Implementação:** o notebook cria as cinco variáveis temporais, remove 66 linhas iniciais sem histórico suficiente e confirma zero valores nulos nas features finais.
- **Resultado:** no teste cronológico final, o pipeline Ridge obteve MAE 4,106, RMSE 4,955 e R² 0,676, com `alpha=10` escolhido por `TimeSeriesSplit`.

O material de apresentação entregue está em `docs/MecaniQA_OAT2_MecaniQA_Salvador.pdf`.

## OAT 3 — Tunando o modelo

### 30/09/2026 — 1ª sessão: comparação de modelos clássicos

- **Equipe da sessão:** William Bichara de Souza **(AUSENTE)** — Piloto; Albert Santos Soares **(AUSENTE)** — Copiloto; Juan Pablo Barros Carvalho — QA; Matheus Espírito Santo dos Santos — Arquiteto; Rafael Pires Araújo — Scrum Master.
- **Decisões da equipe:** comparar `DecisionTreeRegressor` e `RandomForestRegressor`, inicialmente com parâmetros padrão, usando as mesmas features, o mesmo recorte cronológico 80/20 e as mesmas métricas.
- **Entrega solicitada:** treinar dois modelos, calcular RMSE e MAPE e compará-los com o baseline Naive.
- **Implementação:** `notebooks/oat3_pipeline_preditivo.ipynb` reutiliza a limpeza validada da OAT 1, cria features somente com dados anteriores e verifica que o último registro de treino precede o primeiro de teste.
- **Resultado:** Naive — RMSE 8,9248 e MAPE 26,80%; Árvore de Decisão — RMSE 5,4526 e MAPE 17,63%; Random Forest — RMSE 3,5976 e MAPE 12,02%. O Random Forest foi escolhido para a etapa de sintonia.

### 07/10/2026 — 2ª sessão: Grid Search

- **Equipe da sessão:** Rafael Pires Araújo — Piloto; William Bichara de Souza **(AUSENTE)** — Copiloto; Albert Santos Soares — QA; Juan Pablo Barros Carvalho — Arquiteto; Matheus Espírito Santo dos Santos — Scrum Master.
- **Decisões da equipe:** otimizar o modelo vencedor pelo MAPE, usar uma grade pequena e justificável e preservar `TimeSeriesSplit` durante a busca.
- **Entrega solicitada:** declarar a grade de parâmetros, executar `GridSearchCV`, imprimir os melhores parâmetros e comparar o erro com o modelo inicial.
- **Implementação:** a busca avalia 27 combinações de `n_estimators`, `max_depth` e `min_samples_split` sobre os mesmos dados e divisões temporais.
- **Resultado:** os melhores parâmetros foram `n_estimators=300`, `max_depth=None` e `min_samples_split=5`. O modelo ajustado obteve RMSE 3,5611 e MAPE 11,83%, redução de 1,59% no MAPE em relação ao Random Forest inicial.

### 14/10/2026 — 3ª sessão: Random Search e custo computacional

- **Equipe da sessão:** Matheus Espírito Santo dos Santos — Piloto; Rafael Pires Araújo — Copiloto; William Bichara de Souza **(AUSENTE)** — QA; Albert Santos Soares **(AUSENTE)** — Arquiteto; Juan Pablo Barros Carvalho — Scrum Master.
- **Decisões da equipe:** usar Random Search quando houver limitação de recursos e comparar as buscas com o mesmo modelo, espaço de parâmetros, dados, divisões e métrica.
- **Entrega solicitada:** executar `RandomizedSearchCV` com número limitado de tentativas, medir os tempos e registrar o trade-off entre custo e erro.
- **Implementação:** o notebook testa 10 combinações com `random_state` fixo e mede, na mesma execução, os tempos do Grid Search e do Random Search.
- **Resultado:** o Random Search encontrou `n_estimators=100`, `max_depth=10` e `min_samples_split=5`, com RMSE 3,5719 e MAPE 11,87%. Na execução versionada, levou 12,042 s contra 38,472 s do Grid Search, economia de 68,70%, com diferença de apenas 0,04 ponto percentual no MAPE.

## Como executar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
jupyter notebook
```

Inicie o Jupyter pela raiz do projeto e execute todas as células do notebook desejado na ordem. Os caminhos do dataset funcionam quando o Jupyter é iniciado pela raiz ou pela pasta `notebooks`.

Para executar as verificações automatizadas:

```powershell
python -m unittest discover -s tests -p "test_*.py"
powershell -ExecutionPolicy Bypass -File tests/test_oat2_delivery.ps1
```

## Estrutura principal

```text
mecaniQA-salvador/
├── data/
│   └── mecaniqa_dataset.xlsx
├── docs/
│   ├── mecaniQA_oat1_mecaniQA-salvador.pdf
│   ├── MecaniQA_OAT2_MecaniQA_Salvador.pdf
│   └── (slides da OAT 3 ainda não criados)
├── notebooks/
│   ├── oat1_compreensao_baseline.ipynb
│   ├── oat1_pipeline_preditivo.ipynb
│   ├── oat2_pipeline_preditivo.ipynb
│   └── oat3_pipeline_preditivo.ipynb
├── tests/
│   ├── test_oat1_alignment.py
│   ├── test_oat2_delivery.ps1
│   └── test_oat3_tuning.py
├── oat1_processing.py
├── oat3_tuning.py
├── README.md
└── requirements.txt
```

## Critério de entrega e versionamento

A `main` representa a versão consolidada do projeto. Correções relevantes são desenvolvidas em branches separadas para preservar a rastreabilidade das decisões e permitir revisão antes da integração. Slides já entregues não são reescritos retroativamente; quando necessário, o código é corrigido de forma explícita e documentada para corresponder à evidência apresentada.

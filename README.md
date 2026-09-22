# 🔧 MecâniQA Automotive Tech

Projeto desenvolvido para o **Programa de Trainee 2026.2 da MecâniQA Automotive Tech**, com aplicação de Ciência de Dados e Séries Temporais ao histórico de manutenções automotivas.

Nesta etapa da OAT 1, o projeto reúne a compreensão da série diária de trocas de óleo, sua preparação e decomposição, os modelos baseline e a construção de um pipeline preditivo único para evitar vazamento de dados entre treino e teste.

## Contexto do problema

Oficinas e auto centers de Feira de Santana e região enfrentam oscilações na demanda por manutenções preventivas. Picos inesperados podem causar falta de peças e atrasos; períodos de baixa podem gerar ociosidade da equipe. O projeto busca criar uma base analítica capaz de apoiar o planejamento de estoque, escala e atendimento.

A série principal adotada pela equipe é `Trocas_Oleo`, com registros diários de 2024 e 2025.

## O que já foi desenvolvido

### Preparação dos dados

- conversão da coluna `Data` para o tipo temporal;
- ordenação cronológica e definição da data como índice;
- reamostragem da série de trocas de óleo em frequência diária;
- identificação de valores ausentes e outliers;
- criação de variáveis de atraso e médias móveis usando apenas dados passados.

### Análise exploratória e decomposição

- visualização da série temporal;
- separação em tendência, sazonalidade e resíduos;
- decomposição aditiva;
- periodicidade semanal de 7 dias, conforme decisão da equipe;
- baselines Naive e média móvel de 7 dias como referências de comparação;
- médias móveis de 7 e 30 dias como variáveis do pipeline preditivo.

### Atividade de 02/09/2026 — baselines sem vazamento temporal

Na primeira atividade da OAT 2 foram implementados dois modelos simples para
servir como referência nas avaliações seguintes:

- **Naive:** a previsão de cada dia repete o valor observado no dia anterior;
- **média móvel de 7 dias:** a previsão utiliza a média dos sete dias anteriores.

Os dois baselines aplicam `shift(1)` antes de gerar a previsão. Dessa forma, o
resultado do próprio dia e os dados futuros não entram no cálculo. Os valores
ausentes do histórico são preenchidos com `ffill`, que utiliza somente a última
observação conhecida. A série real preserva os valores ausentes para que eles
não sejam interpretados incorretamente como dias com zero trocas.

O notebook `notebooks/oat1_compreensao_baseline.ipynb` apresenta uma tabela com
as previsões e um gráfico sobreposto dos valores reais, do modelo Naive e da
média móvel. Essa implementação é a base para a validação temporal e o cálculo
de MAE, RMSE e MAPE na atividade de 09/09/2026.

### Atividade de 09/09/2026 — validação temporal e métricas

Branch desta atividade: `feat/validacao-temporal-baselines`.

**Brainstorm 1 — a linguagem do cliente. Decisão da equipe:** usamos MAE
como critério principal porque expressa o tamanho médio do erro absoluto na
unidade da demanda. O RMSE também tem essa unidade, mas eleva os erros ao
quadrado antes de calcular a média e extrair a raiz: por isso evidencia mais
um dia com erro de dezenas de manutenções. Apresentamos ambos: MAE para o
erro cotidiano e RMSE para destacar erros grandes. O MAPE complementa a
leitura em percentual, mas pode ser muito sensível a demandas pequenas e
não é definido quando a demanda real é zero.

**Brainstorm 2 — validação no tempo. Decisão da equipe:** usamos
`TimeSeriesSplit(n_splits=5)` com treino expansivo, sem embaralhamento.
O K-Fold tradicional pode treinar com datas posteriores às datas avaliadas,
mesmo sem embaralhar, porque usa os demais blocos como treino. Isso permite
acesso ao futuro e não reproduz a previsão da oficina. Aqui, todo treino
termina antes do início do respectivo teste, preservando tendência e ordem
temporal. Apenas desligar o embaralhamento do K-Fold não resolve o problema.

**Protocolo:** mantivemos Naive e média móvel de sete dias, `shift(1)` e
preenchimento causal por `ffill`, conforme a atividade anterior. Cada previsão
é de **um dia à frente**, feita com o histórico disponível até a véspera.
Durante cada teste, a observação de um dia passa a integrar o histórico para
prever o seguinte; não estamos prevendo todos os 121 dias de uma janela de
uma única vez. Não usamos interpolação na avaliação. Valores reais ausentes
permanecem ausentes e são excluídos das métricas de ambos os modelos nas
mesmas datas. Os zeros continuam no MAE e RMSE e são excluídos somente do
MAPE, com a quantidade de dias efetivamente avaliados impressa por fold.

A implementação está em `validacao_baselines.py` e a seção 7 do notebook
`notebooks/oat1_compreensao_baseline.ipynb` executa o avaliador e imprime o
boletim solicitado. Para executar diretamente com o Python do MSYS2:

```powershell
& C:\msys64\ucrt64\bin\python.exe .\validacao_baselines.py
```

**Resultados medidos na base do projeto:** cinco testes consecutivos de
121 dias, de 06/05/2024 a 31/12/2025. São 605 dias avaliados para MAE/RMSE e
604 para MAPE, pois um dia tem demanda zero. Não há reais ausentes nesses
testes. O boletim agrega todos os erros de teste; não calcula a média simples
dos RMSEs por fold.

| Baseline | MAE (trocas/dia) | RMSE (trocas/dia) | MAPE |
| :-- | --: | --: | --: |
| Naive | 6,6463 | 8,9233 | 32,61% |
| Média móvel de 7 dias | 7,3558 | 8,0889 | 37,18% |

**Escolha:** Naive foi o melhor pelo critério principal, MAE, inclusive nos
cinco folds, e também teve menor MAPE agregado. Seu erro absoluto médio foi
de aproximadamente **6,65 trocas por dia**. A média móvel apresentou menor
RMSE, indicando vantagem quando damos mais peso aos erros grandes. Assim,
Naive será a referência principal, mantendo a média móvel na comparação.

**São bons o suficiente?** Ainda não podemos afirmar: falta definir com a
oficina o erro tolerável e o custo de falta ou excesso de estoque. Essas
métricas medem magnitude, não distinguem falta de sobra. Também não são
uma garantia de desempenho futuro nem uma avaliação final independente da
escolha do baseline.

**Trocas não são litros:** `Trocas_Oleo` mede quantidade de serviços. A base
não informa litros consumidos. Se a oficina fornecer um consumo constante
de `L` litros por troca, o MAE em litros/dia será `6,6463 × L` para o Naive
(e o RMSE também é multiplicado por `L`). Se o consumo variar por veículo,
serão necessários dados de volume para avaliar diretamente o erro em litros.

Validação executada: todas as células de código do notebook, equivalência
da série no CSV e Excel, ordem treino/teste, ausência de datas de teste
repetidas, invariância das previsões anteriores ao alterar o futuro e
conferência das métricas em exemplos com demanda zero.

### Pipeline preditivo

O notebook `notebooks/oat1_pipeline_preditivo.ipynb` implementa a entrega atual com a ordem definida no brainstorm:

1. criar `lag_1` e `lag_7` com `shift(1)` e `shift(7)`;
2. criar as janelas rolantes `rolling_7` e `rolling_30` usando somente o histórico anterior;
3. remover as linhas sem histórico suficiente para a maior janela ou afetadas por nulos da série, evitando preencher features temporais com dados futuros;
4. manter a imputação por mediana aprendida no treino como proteção para eventuais nulos residuais;
5. padronizar as variáveis com `StandardScaler`;
6. aplicar o modelo preditivo Ridge com o hiperparâmetro `alpha` ajustado por validação temporal.

O DataFrame temporal permanente é exibido com `df.head(15)` após o tratamento. A
checagem confirma que `lag_1`, `lag_7`, `rolling_7` e `rolling_30` estão
preenchidas e alinhadas cronologicamente. Como todas as features históricas
usam deslocamento antes do cálculo, nenhuma observação do próprio dia ou do
futuro entra na previsão.

> **Ressalva de alinhamento acadêmico:** os materiais disponibilizados orientam o uso do “modelo preditivo tunado da aula passada”, mas não identificam qual estimador ou quais hiperparâmetros haviam sido definidos. Para viabilizar esta entrega, foi adotada a regressão Ridge como decisão técnica provisória, por ser compatível com a etapa de padronização exigida. O hiperparâmetro `alpha` é selecionado por `GridSearchCV` com `TimeSeriesSplit`. Essa escolha permanece sujeita à confirmação da equipe e do professor e pode ser substituída caso exista uma definição anterior diferente.

O treinamento final é realizado com uma única chamada:

```python
pipeline.fit(X_train, y_train)
```

A divisão entre treino e teste é cronológica, sem embaralhamento. A seleção do hiperparâmetro utiliza `TimeSeriesSplit`, e a avaliação apresenta MAE, RMSE e R², além do gráfico de valores reais contra previsões.

## Como o pipeline evita data leakage

O `SimpleImputer` e o `StandardScaler` executam `fit` apenas no conjunto de treino. Assim, mediana, média e escala ficam armazenadas no pipeline. Ao receber o conjunto de teste ou dados futuros, o pipeline usa somente `transform`, sem recalcular essas estatísticas com informações que não estavam disponíveis no treinamento.

As variáveis históricas também usam deslocamento de um dia (`shift(1)`), garantindo que a previsão de uma data considere apenas o passado.

## Tecnologias

- Python
- Jupyter Notebook
- Pandas
- NumPy
- Matplotlib
- Statsmodels
- Scikit-Learn
- OpenPyXL
- Git e GitHub

## Estrutura do projeto

```text
mecaniQA-salvador/
├── data/
│   └── mecaniqa_dataset.xlsx
├── docs/
│   └── mecaniQA_oat1_mecaniQA-salvador.pdf
├── notebooks/
│   ├── oat1_compreensao_baseline.ipynb
│   └── oat1_pipeline_preditivo.ipynb
├── README.md
└── requirements.txt
```

## Como executar

Crie e ative um ambiente virtual, instale as dependências e abra o Jupyter Notebook:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
jupyter notebook
```

Execute as células dos notebooks na ordem. Os caminhos de leitura foram definidos considerando o Jupyter aberto na pasta `notebooks`.

### Execução pelo VS Code

1. Abra a pasta completa `mecaniQA-salvador` no VS Code.
2. Instale as extensões oficiais **Python** e **Jupyter**, da Microsoft.
3. Abra um terminal na raiz do projeto e execute os comandos de criação do ambiente, ativação e instalação apresentados acima.
4. Abra o notebook desejado.
5. No canto superior direito do notebook, clique em **Selecionar Kernel**.
6. Escolha **Ambientes Python** e selecione o interpretador `.venv\Scripts\python.exe` deste projeto.
7. Confirme que o nome do kernel exibido aponta para `.venv`, e não para o Python da Microsoft Store.
8. Clique em **Executar Tudo** e aguarde a conclusão de todas as células.

Execute primeiro `notebooks/oat1_compreensao_baseline.ipynb` e depois `notebooks/oat1_pipeline_preditivo.ipynb`. Caso o VS Code informe que `ipykernel` não está instalado, confirme que a `.venv` está selecionada e repita `python -m pip install -r requirements.txt` no terminal ativado.

## Equipe e papéis

| Papel | Integrante |
| :-- | :-- |
| Piloto | William Bichara de Souza |
| Copiloto | Rafael Pires Araújo |
| Analista de Qualidade (QA) | Albert Santos Soares |
| Arquiteto | Juan Pablo Barros Carvalho |
| Scrum Master | Matheus Espírito Santo dos Santos |

## Entrega

O desenvolvimento desta etapa foi realizado na branch:

```text
feat/pipeline-preditivo-oat1
```

O repositório segue o padrão `mecaniQA-salvador`. A versão considerada para avaliação deverá ser integrada à branch `main` conforme a orientação da atividade e a revisão da equipe.

O material de apresentação existente está em:

```text
docs/mecaniQA_oat1_mecaniQA-salvador.pdf
```

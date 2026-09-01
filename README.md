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
- baselines Naive, média móvel de 7 dias e média móvel de 30 dias como referências de comparação.

### Pipeline preditivo

O notebook `notebooks/oat1_pipeline_preditivo.ipynb` implementa a entrega atual com a ordem definida no brainstorm:

1. preencher valores nulos com a mediana aprendida no treino;
2. padronizar as variáveis com `StandardScaler`;
3. aplicar o modelo preditivo Ridge com o hiperparâmetro `alpha` ajustado por validação temporal.

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

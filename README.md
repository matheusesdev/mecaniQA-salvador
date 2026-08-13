# 🔧 MecâniQA Automotive Tech

## 📌 OAT 1 — Compreensão e Baseline

Projeto desenvolvido para o **Programa de Trainee 2026.2 da MecâniQA Automotive Tech**, com foco na aplicação de conceitos de **Ciência de Dados e Séries Temporais** para análise do histórico de manutenções automotivas.

---

## 📖 Contexto do Projeto

Os clientes da **MecâniQA**, compostos por oficinas e auto centers de Feira de Santana e região, enfrentam **picos inesperados na demanda por manutenções preventivas** em determinados veículos.

Essas variações podem provocar problemas operacionais, como:

* falta de peças em estoque em períodos de alta demanda;
* ociosidade da equipe de mecânicos em períodos de baixa demanda;
* dificuldade no planejamento de recursos;
* dificuldade em antecipar a demanda por determinados tipos de manutenção.

Diante desse cenário, o projeto tem como objetivo construir a base de um futuro **software preditivo**, começando pela compreensão do histórico de manutenções e pela implementação de modelos simples que funcionem como referência (**Baseline**) para modelos mais avançados no futuro.

Nesta primeira etapa, a equipe atua como o **Time de Ciência de Dados da MecâniQA**, trabalhando principalmente com dados temporais relacionados a **Trocas de Óleo e Manutenções de Motor**.

---

## 🎯 Objetivos

A OAT 1 tem como principais objetivos:

* compreender a estrutura de **dados temporais** e sua indexação por tempo;
* realizar **Análise Exploratória de Dados (EDA)** aplicada a séries temporais;
* identificar componentes como **Tendência, Sazonalidade e Ruído**;
* identificar e tratar **dados ausentes**;
* detectar e tratar **outliers**;
* implementar modelos de previsão **Baseline**;
* utilizar **Médias Móveis** para análise e previsão;
* implementar um modelo **Naive (Ingênuo)**;
* comparar visualmente os valores reais com as previsões produzidas pelos modelos.

---

## 🧹 Preparação e Limpeza dos Dados

Antes das análises, o histórico de manutenções deve ser preparado de maneira que a integridade da série temporal seja preservada.

O processo contempla:

### Dados Ausentes

Identificação de períodos sem registros e aplicação de técnicas adequadas de preenchimento, como:

* interpolação;
* `forward fill`.

### Outliers

Identificação de valores anormais ou inconsistentes na série temporal e aplicação de métodos estatísticos para tratamento desses valores.

---

## 📊 Análise Exploratória de Dados — EDA

A análise exploratória busca compreender o comportamento das manutenções ao longo do tempo.

Entre as análises realizadas estão:

* visualização da série temporal completa;
* análise da evolução das manutenções ao longo dos meses;
* identificação de padrões;
* análise de tendência;
* análise de sazonalidade;
* identificação de ruídos;
* decomposição da série temporal.

A decomposição permite separar a série em componentes como:

**Observado → Tendência → Sazonalidade → Resíduos**

Isso facilita a compreensão dos padrões existentes nos dados antes da aplicação de modelos preditivos.

---

## 🔮 Modelos Baseline

Os modelos Baseline funcionam como um **piso de comparação** para futuros modelos de Machine Learning.

### Modelo Naive

O modelo Naive utiliza uma regra simples:

> A previsão da demanda de amanhã é igual à demanda observada hoje.

Apesar de simples, esse modelo fornece uma referência importante para avaliar se modelos mais avançados realmente apresentam ganhos de desempenho.

### Médias Móveis

Também são utilizadas **Médias Móveis de 7 e 30 dias**.

Essas médias permitem suavizar oscilações da série e gerar previsões considerando o comportamento recente das manutenções.

---

## 📈 Visualizações

O projeto deverá apresentar visualmente:

* série temporal original;
* tendência;
* sazonalidade;
* resíduos/ruídos;
* médias móveis;
* previsões do modelo Naive;
* previsões baseadas em médias móveis;
* comparação entre dados reais e previsões.

---

## 🛠️ Tecnologias

O projeto é desenvolvido utilizando o ecossistema Python para análise de dados.

Principais tecnologias e ferramentas utilizadas:

* **Python**
* **Jupyter Notebook**
* **Pandas**
* **NumPy**
* **Matplotlib**
* **Statsmodels**
* **Git**
* **GitHub**

---

## 📂 Estrutura do Projeto

A estrutura do repositório segue:

```text
mecaniQA-salvador/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── mecaniqa_dataset.xlsx
│
└── notebooks/
    └── oat1_compreensao_baseline.ipynb
```

> A estrutura poderá sofrer alterações durante o desenvolvimento do projeto.

---

## 👥 Equipe

| Membro                            |
| :-------------------------------- |
| Albert Santos Soares              |
| Juan Pablo Barros Carvalho        |
| Matheus Espírito Santo dos Santos |
| Rafael Pires Araujo               |
| William Bichara de Souza          |

---

## 📦 Entrega

O projeto será desenvolvido e versionado utilizando **Git/GitHub**.

O repositório segue o padrão definido para a atividade:

```text
mecaniQA-salvador
```

A versão considerada para avaliação será aquela disponível na branch:

```text
main
```

Também fará parte do repositório a apresentação do projeto seguindo o padrão:

```text
mecaniQA_oat1_salvador.pdf
```

---


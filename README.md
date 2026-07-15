# IC - Infectologia

Projeto de pesquisa sobre Resistência Antimicrobiana (RAM) e seus
impulsionadores exógenos (climáticos, ambientais e socioeconômicos),
combinando revisão bibliográfica automatizada, um agente de IA para
extração semântica, engenharia de dados espaço-temporais e modelagem
preditiva.

## Como o projeto está organizado

O trabalho é dividido em **Blocos** (grandes etapas) e cada Bloco em
**Microtarefas** (entregas menores e independentes). Cada microtarefa vive
na sua própria pasta, com seu próprio código e seu próprio `README.md`
explicando o que ela faz e como rodar:

```
bloco_N_nome/
└── microtarefa_N_M_nome/
    ├── ...código...
    ├── README.md      ← como rodar essa microtarefa especificamente
    └── output/        ← resultados gerados por ela (nao versionado no git)
```

Todo o projeto compartilha **um único ambiente virtual Python** (`venv/`, na
raiz) e **um único `requirements.txt`**, que vai crescendo conforme novas
microtarefas são adicionadas — em vez de reinstalar dependências em cada
pasta. Para configurar:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Status do projeto

| Bloco | Microtarefa | Status |
|---|---|---|
| **1. Revisão Bibliográfica Automatizada** | | |
| | [1.1 Busca e Descoberta Automatizada](bloco_1_revisao_bibliografica_automatizada/microtarefa_1_1_busca_descoberta/) | ✅ Concluída |
| | [1.2 Coleta de Texto Completo](bloco_1_revisao_bibliografica_automatizada/microtarefa_1_2_coleta_texto_completo/) | ⏳ Não iniciada |
| | [1.3 Parsing e Pré-processamento de Documentos](bloco_1_revisao_bibliografica_automatizada/microtarefa_1_3_parsing_preprocessamento/) | ⏳ Não iniciada |
| | [1.4 Extração Semântica via RAG (Agente LLM)](bloco_1_revisao_bibliografica_automatizada/microtarefa_1_4_extracao_semantica_rag/) | ⏳ Não iniciada |
| **2. [Coleta de Dados Exógenos](bloco_2_coleta_dados_exogenos/)** | *(microtarefas a definir)* | ⏳ Não iniciado |
| **3. [Arquitetura do Agente de IA](bloco_3_arquitetura_agente_ia/)** | *(microtarefas a definir)* | ⏳ Não iniciado |
| **4. [Fusão de Dados Espaço-Temporais](bloco_4_fusao_dados_espaco_temporais/)** | *(microtarefas a definir)* | ⏳ Não iniciado |
| **5. [Modelagem Preditiva e Avaliação](bloco_5_modelagem_preditiva/)** | *(microtarefas a definir)* | ⏳ Não iniciado |

Os nomes dos blocos/microtarefas são provisórios — tanto os títulos quanto o
escopo exato de cada um devem evoluir ao longo do projeto. Atualize esta
tabela conforme o trabalho avança.

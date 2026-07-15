[Versão em português](README.pt-br.md)

# AMR-LLM-Extractor

Research project on Antimicrobial Resistance (AMR) and its exogenous drivers
(climatic, environmental, and socioeconomic), combining automated literature
review, an LLM-based agent for semantic extraction, spatio-temporal data
engineering, and predictive modeling. Originally developed as an undergraduate
research project (*Iniciação Científica*, a Brazilian research program) in
Infectious Diseases.

## Structure

The work is split into Blocks (major stages), each broken down into
Microtasks (smaller, self-contained deliverables). Each microtask lives in
its own folder, with its own code and its own README explaining what it does
and how to run it:

```
block_N_name/
└── microtask_N_M_name/
    ├── ...code...
    ├── README.md      -> how to run this specific microtask
    └── output/        -> results it generates (not tracked in git)
```

Note: folder names on disk are in Portuguese (e.g.
`bloco_1_revisao_bibliografica_automatizada`); the diagram above just
illustrates the pattern in English.

The whole project shares a single Python virtual environment (`venv/`, at the
root) and a single `requirements.txt`, which grows as new microtasks are
added, instead of reinstalling dependencies in every folder. To set it up:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Status

Block 1 - Automated Literature Review
- [1.1 Search & Discovery Engineering](bloco_1_revisao_bibliografica_automatizada/microtarefa_1_1_busca_descoberta/) - done
- [1.2 Full-Text Collection](bloco_1_revisao_bibliografica_automatizada/microtarefa_1_2_coleta_texto_completo/) - not started
- [1.3 Document Parsing & Preprocessing](bloco_1_revisao_bibliografica_automatizada/microtarefa_1_3_parsing_preprocessamento/) - not started
- [1.4 Semantic Extraction via RAG (LLM Agent)](bloco_1_revisao_bibliografica_automatizada/microtarefa_1_4_extracao_semantica_rag/) - not started

Block 2 - [Exogenous Data Collection](bloco_2_coleta_dados_exogenos/) - not started, microtasks not yet defined

Block 3 - [AI Agent Architecture](bloco_3_arquitetura_agente_ia/) - not started, microtasks not yet defined

Block 4 - [Spatio-Temporal Data Fusion](bloco_4_fusao_dados_espaco_temporais/) - not started, microtasks not yet defined

Block 5 - [Predictive Modeling & Evaluation](bloco_5_modelagem_preditiva/) - not started, microtasks not yet defined

Block/microtask names are provisional and will likely evolve as the project
progresses.

# Microtarefa 1.1 — Busca e Descoberta Automatizada

_Bloco 1 — Revisão Bibliográfica Automatizada_

Pipeline de coleta automatizada (PubMed + OpenAlex) sobre RAM x impulsionadores
exógenos (climáticos, ambientais, socioeconômicos), custo financeiro zero.

## Estrutura

- `config.py` — e-mail/API key, período, queries booleanas, parâmetros de rede.
- `pubmed_client.py` — busca via Biopython/Entrez.
- `openalex_client.py` — busca via OpenAlex REST API (paginação por cursor).
- `data_pipeline.py` — consolidação, limpeza, deduplicação por DOI, exportação.
- `main.py` — orquestra o pipeline ponta a ponta.

## Por que OpenAlex em vez de Google Scholar

O Google Scholar não tem API oficial — qualquer coleta automatizada depende de
scraping não autorizado (ex.: biblioteca `scholarly`), sujeito a bloqueio de IP
mesmo com proxies gratuitos ou Tor (o Google inclusive bloqueia ativamente
nós de saída do Tor), sem rate limit documentado e sem contrato de API
estável — ruim para um pipeline que precisa ser reproduzível.

A **OpenAlex** (openalex.org) é um catálogo aberto com API REST oficial,
gratuita, sem necessidade de chave, cobertura comparável à do Scholar, rate
limit documentado e generoso (10 req/s, 100k req/dia no modo "polite pool"),
e já devolve DOI, abstract e ano estruturados. Resultado: mesmo custo zero,
porém sem nenhuma engenharia de anti-bloqueio (proxy/Tor/atrasos aleatórios).

## 1. Ambiente Python

O projeto usa **um único ambiente virtual compartilhado**, na raiz do
repositório (não dentro desta pasta), para evitar reinstalar dependências em
cada microtarefa:

```
cd ..\..                       # volta para a raiz do projeto
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Depois disso, volte para esta pasta para rodar o script (o `venv` continua
ativo, não importa em qual pasta você esteja):

```
cd bloco_1_revisao_bibliografica_automatizada\microtarefa_1_1_busca_descoberta
```

Edite `config.py` (ou defina a variável de ambiente `ENTREZ_EMAIL`) com o
e-mail usado tanto nas requisições ao NCBI (obrigatório por política da API)
quanto no "polite pool" da OpenAlex (opcional, mas recomendado — melhora o
rate limit). Uma `ENTREZ_API_KEY` (gratuita, gerada na conta NCBI) também é
opcional e eleva o limite do PubMed de 3 para 10 requisições/segundo.

Não é necessário configurar proxy, VPN ou Tor — ambas as fontes são
consultadas via API oficial, sem scraping.

## 2. Executar

```
python main.py                # PubMed + OpenAlex
python main.py --apenas-pubmed  # apenas PubMed
```

Saída em `output/ram_impulsionadores_exogenos.csv` e `.json`.

## Limitações conhecidas

- A cobertura da OpenAlex é ampla, mas não idêntica à do Google Scholar —
  algumas teses/dissertações e literatura cinzenta podem não estar indexadas.
- As queries da OpenAlex usam a minilinguagem de busca da própria API
  (espaço = AND, `|` = OR, aspas = frase exata), diferente da sintaxe de
  campos do PubMed (`[MeSH Terms]`/`[tiab]`), mas cobrem os mesmos três eixos
  temáticos.

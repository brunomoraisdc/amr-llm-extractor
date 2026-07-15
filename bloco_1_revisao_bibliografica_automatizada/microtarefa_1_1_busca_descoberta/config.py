"""
Configuracao central do pipeline de busca - Microtarefa 1.1.
Projeto: impulsionadores exogenos (climaticos, ambientais, socioeconomicos) da RAM.
"""
import os
from pathlib import Path

# Ancora os caminhos na pasta deste arquivo, para que "output/" va sempre
# para dentro desta microtarefa, nao importa de onde o comando "python" e chamado.
BASE_DIR = Path(__file__).resolve().parent

# --- Identificacao obrigatoria junto ao NCBI (E-utilities) ---
ENTREZ_EMAIL = os.getenv("ENTREZ_EMAIL", "brunomoraisdc@gmail.com")
ENTREZ_API_KEY = os.getenv("ENTREZ_API_KEY")  # opcional; eleva o limite de 3 para 10 req/s

# --- Janela temporal do estudo ---
YEAR_MIN = 2015
YEAR_MAX = 2026
PUBMED_MINDATE = f"{YEAR_MIN}/01/01"
PUBMED_MAXDATE = f"{YEAR_MAX}/12/31"

# --- Volume de resultados ---
PUBMED_RETMAX = 500        # numero maximo de PMIDs recuperados
PUBMED_BATCH_SIZE = 200    # tamanho do lote no efetch (NCBI recomenda <=500 por chamada)

# --- Strings de busca (Eixo 1: Biologico x Eixo 2: Climatico/Ambiental x Eixo 3: Socioeconomico) ---
PUBMED_QUERY = """
(
  "Anti-Bacterial Agents"[MeSH Terms] OR "Drug Resistance, Bacterial"[MeSH Terms]
  OR "Drug Resistance, Microbial"[MeSH Terms] OR "antimicrobial resistance"[tiab]
  OR "antibiotic resistance"[tiab] OR "multidrug resistan*"[tiab] OR "ESKAPE"[tiab]
  OR "Enterococcus faecium"[tiab] OR "Staphylococcus aureus"[tiab]
  OR "Klebsiella pneumoniae"[tiab] OR "Acinetobacter baumannii"[tiab]
  OR "Pseudomonas aeruginosa"[tiab] OR "Enterobacter"[tiab]
)
AND
(
  "Climate Change"[MeSH Terms] OR "climate change"[tiab] OR "global warming"[tiab]
  OR "temperature"[tiab] OR "precipitation"[tiab] OR "rainfall"[tiab]
  OR "Water Quality"[MeSH Terms] OR "water quality"[tiab] OR "environmental contamination"[tiab]
)
AND
(
  "Socioeconomic Factors"[MeSH Terms] OR "socioeconomic"[tiab] OR "socio-economic"[tiab]
  OR "Sanitation"[MeSH Terms] OR "sanitation"[tiab] OR "Public Health"[MeSH Terms]
  OR "public health"[tiab] OR "DATASUS"[tiab] OR "Brazil"[tiab] OR "Brasil"[tiab]
)
""".replace("\n", " ").strip()

# --- OpenAlex: segunda fonte gratuita, no lugar do Google Scholar ---
# OpenAlex (https://openalex.org) e uma API REST oficial e gratuita, sem
# necessidade de chave de autenticacao. Diferente do scraping do Google
# Scholar, tem contrato estavel e rate limit documentado, o que dispensa
# qualquer camada de anti-bloqueio (proxy/Tor/atrasos aleatorios).
OPENALEX_BASE_URL = "https://api.openalex.org/works"
OPENALEX_MAILTO = ENTREZ_EMAIL  # identifica o cliente para o "polite pool" (rate limit maior)
OPENALEX_MAX_RESULTS = 300
OPENALEX_PER_PAGE = 100          # maximo permitido pela API por pagina
OPENALEX_REQUEST_DELAY = 0.15    # segundos entre paginas (folga confortavel na polite pool)

# Mesma logica de 3 eixos do PubMed, usando a minilinguagem de busca do
# OpenAlex: espaco = AND, pipe "|" = OR, aspas = frase exata, virgula entre
# filtros = AND entre eixos.
_OPENALEX_AXIS_BIOLOGICO = (
    '"antimicrobial resistance"|"antibiotic resistance"|"multidrug resistance"|ESKAPE'
    '|"Enterococcus faecium"|"Staphylococcus aureus"|"Klebsiella pneumoniae"'
    '|"Acinetobacter baumannii"|"Pseudomonas aeruginosa"|Enterobacter'
)
_OPENALEX_AXIS_CLIMATICO = (
    '"climate change"|"global warming"|temperature|precipitation|rainfall'
    '|"water quality"|"environmental contamination"'
)
_OPENALEX_AXIS_SOCIOECONOMICO = (
    'socioeconomic|"socio-economic"|sanitation|"public health"|DATASUS|Brazil|Brasil'
)

OPENALEX_FILTER = (
    f"title_and_abstract.search:{_OPENALEX_AXIS_BIOLOGICO},"
    f"title_and_abstract.search:{_OPENALEX_AXIS_CLIMATICO},"
    f"title_and_abstract.search:{_OPENALEX_AXIS_SOCIOECONOMICO},"
    f"from_publication_date:{YEAR_MIN}-01-01,"
    f"to_publication_date:{YEAR_MAX}-12-31"
)

# --- Saida ---
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_CSV = "ram_impulsionadores_exogenos.csv"
OUTPUT_JSON = "ram_impulsionadores_exogenos.json"

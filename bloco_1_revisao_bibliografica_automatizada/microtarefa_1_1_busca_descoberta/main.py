"""
Microtarefa 1 - Engenharia de Busca e Descoberta Automatizada.

Orquestra a coleta no PubMed e na OpenAlex, consolida os metadados,
limpa e deduplica por DOI, e exporta o resultado final para .csv e .json.

Uso:
    python main.py                  # PubMed + OpenAlex
    python main.py --apenas-pubmed  # apenas PubMed
"""
import argparse
import logging

from data_pipeline import build_dataframe, clean_and_deduplicate, export
from openalex_client import search_openalex
from pubmed_client import search_pubmed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("main")


def run(include_openalex: bool = True) -> None:
    pubmed_records = search_pubmed()

    openalex_records = []
    if include_openalex:
        openalex_records = search_openalex()
    else:
        logger.info("Coleta na OpenAlex desativada (--apenas-pubmed).")

    df = build_dataframe(pubmed_records, openalex_records)
    df_clean = clean_and_deduplicate(df)

    logger.info(
        "Resumo: %d (PubMed) + %d (OpenAlex) = %d brutos -> %d apos limpeza/deduplicacao.",
        len(pubmed_records), len(openalex_records), len(df), len(df_clean),
    )

    export(df_clean)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de busca RAM x impulsionadores exogenos.")
    parser.add_argument(
        "--apenas-pubmed",
        action="store_true",
        help="Executa apenas a coleta no PubMed, pulando a OpenAlex.",
    )
    args = parser.parse_args()
    run(include_openalex=not args.apenas_pubmed)

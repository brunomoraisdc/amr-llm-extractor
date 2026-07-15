"""
Cliente de busca no PubMed via NCBI Entrez (Biopython).

Respeita os limites de taxa da API E-utilities do NCBI:
- 3 requisicoes/segundo sem chave de API;
- 10 requisicoes/segundo com chave de API (ENTREZ_API_KEY).
"""
import logging
import time
from typing import Any, Dict, List

from Bio import Entrez

import config

logger = logging.getLogger(__name__)

_REQUEST_INTERVAL = 0.11 if config.ENTREZ_API_KEY else 0.34


def _throttle() -> None:
    time.sleep(_REQUEST_INTERVAL)


def _configure_entrez() -> None:
    if not config.ENTREZ_EMAIL:
        raise ValueError("ENTREZ_EMAIL precisa estar definido em config.py (exigencia do NCBI).")
    Entrez.email = config.ENTREZ_EMAIL
    if config.ENTREZ_API_KEY:
        Entrez.api_key = config.ENTREZ_API_KEY


def _search_ids(query: str, mindate: str, maxdate: str, retmax: int) -> Dict[str, Any]:
    handle = Entrez.esearch(
        db="pubmed",
        term=query,
        mindate=mindate,
        maxdate=maxdate,
        datetype="pdat",
        retmax=retmax,
        usehistory="y",
    )
    try:
        record = Entrez.read(handle)
    finally:
        handle.close()
    _throttle()
    return record


def _fetch_batch(webenv: str, query_key: str, start: int, batch_size: int) -> List[Dict[str, Any]]:
    handle = Entrez.efetch(
        db="pubmed",
        rettype="abstract",
        retmode="xml",
        retstart=start,
        retmax=batch_size,
        webenv=webenv,
        query_key=query_key,
    )
    try:
        data = Entrez.read(handle)
    finally:
        handle.close()
    _throttle()
    return data.get("PubmedArticle", [])


def _extract_doi(article_ids: List[Any]) -> str:
    for aid in article_ids:
        if getattr(aid, "attributes", {}).get("IdType") == "doi":
            return str(aid)
    return ""


def _extract_abstract(article: Dict[str, Any]) -> str:
    abstract_text = article.get("Abstract", {}).get("AbstractText", [])
    if not abstract_text:
        return ""
    parts = []
    for piece in abstract_text:
        label = getattr(piece, "attributes", {}).get("Label")
        text = str(piece)
        parts.append(f"{label}: {text}" if label else text)
    return " ".join(parts)


def _extract_authors(article: Dict[str, Any]) -> str:
    author_list = article.get("AuthorList", [])
    names = []
    for author in author_list:
        last = author.get("LastName", "")
        initials = author.get("Initials", "")
        if last:
            names.append(f"{last} {initials}".strip())
        elif "CollectiveName" in author:
            names.append(str(author["CollectiveName"]))
    return "; ".join(names)


def _extract_year(article: Dict[str, Any]) -> str:
    pub_date = article.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
    year = pub_date.get("Year")
    if year:
        return str(year)
    medline_date = pub_date.get("MedlineDate", "")
    return medline_date[:4] if medline_date else ""


def _parse_record(pubmed_article: Dict[str, Any]) -> Dict[str, Any]:
    medline = pubmed_article["MedlineCitation"]
    article = medline["Article"]
    pmid = str(medline["PMID"])
    article_ids = pubmed_article.get("PubmedData", {}).get("ArticleIdList", [])

    return {
        "DOI": _extract_doi(article_ids),
        "Titulo": str(article.get("ArticleTitle", "")),
        "Autores": _extract_authors(article),
        "Ano": _extract_year(article),
        "Resumo": _extract_abstract(article),
        "Base": "PubMed",
        "URL": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }


def search_pubmed(
    query: str = config.PUBMED_QUERY,
    mindate: str = config.PUBMED_MINDATE,
    maxdate: str = config.PUBMED_MAXDATE,
    retmax: int = config.PUBMED_RETMAX,
    batch_size: int = config.PUBMED_BATCH_SIZE,
) -> List[Dict[str, Any]]:
    """Busca no PubMed e retorna uma lista de dicionarios com metadados padronizados."""
    _configure_entrez()
    logger.info("Consultando PubMed (%s a %s)...", mindate, maxdate)

    try:
        search_record = _search_ids(query, mindate, maxdate, retmax)
    except Exception:
        logger.exception("Falha ao consultar PubMed (esearch).")
        return []

    total = int(search_record.get("Count", 0))
    webenv = search_record["WebEnv"]
    query_key = search_record["QueryKey"]
    n_to_fetch = min(total, retmax)
    logger.info("PubMed reportou %d resultados; recuperando ate %d.", total, n_to_fetch)

    records: List[Dict[str, Any]] = []
    for start in range(0, n_to_fetch, batch_size):
        current_batch = min(batch_size, n_to_fetch - start)
        try:
            articles = _fetch_batch(webenv, query_key, start, current_batch)
        except Exception:
            logger.exception("Falha ao recuperar lote PubMed a partir do indice %d; pulando.", start)
            continue

        for article in articles:
            try:
                records.append(_parse_record(article))
            except Exception:
                logger.warning("Falha ao interpretar um registro PubMed; ignorado.", exc_info=True)

    logger.info("PubMed: %d registros extraidos com sucesso.", len(records))
    return records

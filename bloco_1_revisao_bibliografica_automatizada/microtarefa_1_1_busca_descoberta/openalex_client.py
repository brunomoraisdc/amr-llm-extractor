"""
Cliente de busca na OpenAlex API - segunda fonte gratuita, no lugar do
Google Scholar.

A OpenAlex (https://openalex.org) e um catalogo aberto mantido sem fins
lucrativos, com API REST oficial e sem necessidade de chave de autenticacao.
Ao contrario do scraping do Google Scholar, tem contrato de API estavel e
rate limit documentado (~10 req/s / 100k req/dia no "polite pool", ativado
ao identificar o cliente via `mailto`), o que elimina a necessidade de
proxies, Tor ou atrasos aleatorios para mitigar bloqueios.
"""
import logging
import time
from typing import Any, Dict, List, Optional

import requests

import config

logger = logging.getLogger(__name__)


def _reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    # A OpenAlex nao devolve o abstract como texto corrido, e sim como um
    # indice invertido (palavra -> posicoes), por questoes de direitos
    # autorais de indexacao. Reconstruimos o texto a partir das posicoes.
    if not inverted_index:
        return ""
    max_pos = max(pos for positions in inverted_index.values() for pos in positions)
    words = [""] * (max_pos + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words)


def _extract_authors(work: Dict[str, Any]) -> str:
    names = []
    for authorship in work.get("authorships", []):
        name = authorship.get("author", {}).get("display_name")
        if name:
            names.append(name)
    return "; ".join(names)


def _extract_doi(work: Dict[str, Any]) -> str:
    doi = work.get("doi") or ""
    return doi.replace("https://doi.org/", "").strip()


def _extract_url(work: Dict[str, Any]) -> str:
    doi = work.get("doi")
    if doi:
        return doi
    landing_page = (work.get("primary_location") or {}).get("landing_page_url")
    return landing_page or work.get("id", "")


def _parse_work(work: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "DOI": _extract_doi(work),
        "Titulo": work.get("title") or work.get("display_name") or "",
        "Autores": _extract_authors(work),
        "Ano": str(work.get("publication_year") or ""),
        "Resumo": _reconstruct_abstract(work.get("abstract_inverted_index")),
        "Base": "OpenAlex",
        "URL": _extract_url(work),
    }


def search_openalex(
    filter_query: str = config.OPENALEX_FILTER,
    max_results: int = config.OPENALEX_MAX_RESULTS,
    per_page: int = config.OPENALEX_PER_PAGE,
) -> List[Dict[str, Any]]:
    """Busca na OpenAlex (paginacao por cursor) e retorna metadados padronizados."""
    logger.info("Consultando OpenAlex...")

    records: List[Dict[str, Any]] = []
    cursor = "*"
    first_page = True
    session = requests.Session()

    while cursor and len(records) < max_results:
        params = {
            "filter": filter_query,
            "per-page": min(per_page, max_results - len(records)),
            "cursor": cursor,
            "mailto": config.OPENALEX_MAILTO,
        }
        try:
            response = session.get(config.OPENALEX_BASE_URL, params=params, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            logger.exception("Falha de conexao com a OpenAlex; encerrando coleta.")
            break

        payload = response.json()
        if first_page:
            total = payload.get("meta", {}).get("count", 0)
            logger.info("OpenAlex reportou %d resultados; recuperando ate %d.", total, max_results)
            first_page = False

        results = payload.get("results", [])
        if not results:
            break

        for work in results:
            try:
                records.append(_parse_work(work))
            except Exception:
                logger.warning("Falha ao interpretar um registro da OpenAlex; ignorado.", exc_info=True)

        cursor = payload.get("meta", {}).get("next_cursor")
        time.sleep(config.OPENALEX_REQUEST_DELAY)

    logger.info("OpenAlex: %d registros extraidos com sucesso.", len(records))
    return records

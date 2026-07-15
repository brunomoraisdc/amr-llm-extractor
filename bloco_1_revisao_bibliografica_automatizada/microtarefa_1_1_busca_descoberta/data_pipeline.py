"""
Consolidacao, limpeza, deduplicacao e exportacao dos metadados coletados
a partir do PubMed e do Google Scholar.
"""
import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

import config

logger = logging.getLogger(__name__)

COLUMNS = ["DOI", "Titulo", "Autores", "Ano", "Resumo", "Base", "URL"]

_DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$")


def _normalize_doi(raw: Any) -> Optional[str]:
    """Normaliza o DOI (minusculas, sem prefixo de URL) e descarta valores mal formados."""
    if raw is None:
        return None
    doi = str(raw).strip().lower()
    if not doi:
        return None
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    doi = doi.strip().strip(".")
    return doi if _DOI_PATTERN.match(doi) else None


def _normalize_title(raw: Any) -> str:
    """Normaliza o titulo para uso como chave secundaria de deduplicacao."""
    title = str(raw or "").lower()
    title = re.sub(r"[^\w\s]", "", title)
    return re.sub(r"\s+", " ", title).strip()


def build_dataframe(pubmed_records: List[Dict], scholar_records: List[Dict]) -> pd.DataFrame:
    """Consolida os registros de ambas as fontes em um unico DataFrame padronizado."""
    all_records = list(pubmed_records) + list(scholar_records)
    if not all_records:
        return pd.DataFrame(columns=COLUMNS)

    df = pd.DataFrame(all_records)
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""
    df = df[COLUMNS]

    df["DOI"] = df["DOI"].apply(_normalize_doi)
    df["Titulo"] = df["Titulo"].fillna("").astype(str).str.strip()
    df["Ano"] = df["Ano"].fillna("").astype(str).str.extract(r"(\d{4})")[0]
    return df


def clean_and_deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e deduplica o DataFrame usando o DOI como chave primaria.

    Registros sem DOI (comuns no Google Scholar, que raramente o expoe) sao
    deduplicados por titulo normalizado, tanto entre si quanto contra
    registros com DOI, para evitar duplicidade entre as duas fontes.
    """
    if df.empty:
        return df

    df = df.copy()
    df["_titulo_norm"] = df["Titulo"].apply(_normalize_title)

    # Remove linhas sem titulo e sem DOI (lixo de parsing).
    df = df[~((df["DOI"].isna()) & (df["_titulo_norm"] == ""))]

    # Em caso de duplicidade, prioriza o PubMed (metadados estruturados mais confiaveis).
    df["_prioridade"] = (df["Base"] != "PubMed").astype(int)
    df = df.sort_values("_prioridade")

    com_doi = df[df["DOI"].notna()].drop_duplicates(subset="DOI", keep="first")
    sem_doi = df[df["DOI"].isna()]

    titulos_com_doi = set(com_doi["_titulo_norm"])
    sem_doi = sem_doi[~sem_doi["_titulo_norm"].isin(titulos_com_doi)]
    sem_doi = sem_doi.drop_duplicates(subset="_titulo_norm", keep="first")

    result = pd.concat([com_doi, sem_doi], ignore_index=True)
    result = result.drop(columns=["_titulo_norm", "_prioridade"])
    result = result.sort_values(["Ano", "Titulo"], ascending=[False, True], na_position="last")
    return result.reset_index(drop=True)


def export(df: pd.DataFrame, output_dir: Union[str, Path] = config.OUTPUT_DIR) -> None:
    """Exporta o DataFrame final para CSV (utf-8-sig) e JSON (utf-8, legivel)."""
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, config.OUTPUT_CSV)
    json_path = os.path.join(output_dir, config.OUTPUT_JSON)

    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    records = df.to_dict(orient="records")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    logger.info("Exportado: %s (%d linhas)", csv_path, len(df))
    logger.info("Exportado: %s (%d linhas)", json_path, len(df))

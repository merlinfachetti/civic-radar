"""Cebraspe HTML parser.

The Cebraspe site lists open contests as ``<li class="card-concurso">`` nodes
on the index page. This parser extracts the basics needed to build a
:class:`ParsedOpportunity`.

Layout assumptions (versioned via ``parser_version``):
- ``.card-concurso`` is the row
- ``.card-titulo`` carries the title
- ``.card-link`` points to the detail URL
- ``.orgao``, ``.cargo``, ``.escolaridade``, ``.salario``, ``.vagas``, ``.uf``,
  ``.inscricoes`` carry the meta fields.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal
from typing import ClassVar
from urllib.parse import urljoin

from selectolax.parser import HTMLParser, Node

from crawlers.core.base import BaseParser
from crawlers.core.models import ParsedOpportunity, RawSnapshot

_REGISTRATION_RE = re.compile(
    r"Inscri[cç][oõ]es:\s*(\d{2}/\d{2}/\d{4})\s*a\s*(\d{2}/\d{2}/\d{4})",
    re.IGNORECASE,
)
_SALARY_RE = re.compile(r"R\$\s*([\d.]+,\d{2})(?:\s*a\s*R\$\s*([\d.]+,\d{2}))?")
_VACANCIES_RE = re.compile(r"(\d+)\s+vaga", re.IGNORECASE)


def _text(node: Node | None) -> str | None:
    if node is None:
        return None
    return BaseParser.coerce_text(node.text())


def _select(card: Node, css: str) -> Node | None:
    return card.css_first(css)


def _parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError:
        return None


def _parse_salary(text: str | None) -> tuple[Decimal | None, Decimal | None]:
    if not text:
        return None, None
    match = _SALARY_RE.search(text)
    if not match:
        return None, None
    low = _to_decimal(match.group(1))
    high = _to_decimal(match.group(2)) if match.group(2) else low
    return low, high


def _to_decimal(value: str) -> Decimal:
    cleaned = value.replace(".", "").replace(",", ".")
    return Decimal(cleaned)


def _parse_vacancies(text: str | None) -> int | None:
    if not text:
        return None
    match = _VACANCIES_RE.search(text)
    return int(match.group(1)) if match else None


def _infer_area(title: str, position: str | None) -> str | None:
    haystack = f"{title} {position or ''}".lower()
    if any(token in haystack for token in ("ti", "sistema", "software", "desenvolv", "tecnologia")):
        return "tecnologia"
    if any(token in haystack for token in ("polícia", "policia", "segurança", "agente")):
        return "seguranca_publica"
    if any(token in haystack for token in ("audit", "fiscal", "tributário", "tributario")):
        return "fiscal"
    if any(token in haystack for token in ("procurador", "juíz", "juiz", "advogado", "jurídic")):
        return "juridica"
    if any(token in haystack for token in ("médico", "medico", "enferm", "saúde", "saude")):
        return "saude"
    return None


class Parser(BaseParser):
    source_id: ClassVar[str] = "cebraspe"
    parser_version: ClassVar[str] = "1.0.0"

    def parse(self, snapshot: RawSnapshot) -> list[ParsedOpportunity]:
        tree = HTMLParser(snapshot.text)
        cards = tree.css("li.card-concurso")
        results: list[ParsedOpportunity] = []

        for card in cards:
            title = _text(_select(card, ".card-titulo"))
            if not title:
                continue

            link_node = _select(card, "a.card-link")
            href = link_node.attributes.get("href") if link_node else None
            detail_url = urljoin(snapshot.url, href) if href else snapshot.url

            organization = _text(_select(card, ".orgao")) or title
            position = _text(_select(card, ".cargo"))
            education_text = _text(_select(card, ".escolaridade"))
            salary_text = _text(_select(card, ".salario"))
            vacancies_text = _text(_select(card, ".vagas"))
            uf = _text(_select(card, ".uf"))
            registration_text = _text(_select(card, ".inscricoes"))

            salary_min, salary_max = _parse_salary(salary_text)
            vacancies = _parse_vacancies(vacancies_text)

            reg_start = reg_end = None
            if registration_text and (match := _REGISTRATION_RE.search(registration_text)):
                reg_start = _parse_date(match.group(1))
                reg_end = _parse_date(match.group(2))

            results.append(
                ParsedOpportunity(
                    title=title,
                    organization=organization,
                    board="cebraspe",
                    area=_infer_area(title, position),
                    position_name=position,
                    education_level=education_text,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    vacancies=vacancies,
                    state=uf,
                    status="open",
                    registration_start_date=reg_start,
                    registration_end_date=reg_end,
                    source_url=detail_url,
                    confidence_level="high",
                )
            )

        return results

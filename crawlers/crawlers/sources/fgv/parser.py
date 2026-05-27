"""FGV CONHECIMENTO HTML parser.

Layout assumptions (versioned via ``parser_version``):
- Each entry is an ``article.processo`` node.
- Title is ``h2.titulo a`` (or text).
- Meta data is a ``dl.detalhes`` with alternating ``dt``/``dd`` pairs.
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

_SALARY_RE = re.compile(r"R\$\s*([\d.]+,\d{2})(?:\s*a\s*R\$\s*([\d.]+,\d{2}))?")
_DATE_RANGE_RE = re.compile(r"(\d{2}/\d{2}/\d{4})\s*[—\-–to]+\s*(\d{2}/\d{2}/\d{4})")


def _text(node: Node | None) -> str | None:
    if node is None:
        return None
    return BaseParser.coerce_text(node.text())


def _to_decimal(value: str) -> Decimal:
    return Decimal(value.replace(".", "").replace(",", "."))


def _parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError:
        return None


def _parse_kv(article: Node) -> dict[str, str]:
    dl = article.css_first("dl.detalhes")
    if dl is None:
        return {}

    pairs: dict[str, str] = {}
    children = [c for c in dl.iter() if c.tag in {"dt", "dd"}]
    key: str | None = None
    for child in children:
        text = _text(child) or ""
        if child.tag == "dt":
            key = text.lower().rstrip(":")
        elif key is not None:
            pairs[key] = text
            key = None
    return pairs


def _split_local(value: str | None) -> tuple[str | None, str | None]:
    if not value:
        return None, None
    if "/" in value:
        city, uf = value.rsplit("/", 1)
        return city.strip(), uf.strip().upper()
    return value.strip(), None


def _infer_area(title: str, position: str | None) -> str | None:
    haystack = f"{title} {position or ''}".lower()
    if any(t in haystack for t in ("ti", "sistema", "software", "desenvolv", "tecnologia")):
        return "tecnologia"
    if any(t in haystack for t in ("médico", "medico", "enferm", "saúde", "saude", "farmac")):
        return "saude"
    if any(t in haystack for t in ("procurador", "advogado", "jurídic", "juridica")):
        return "juridica"
    if any(t in haystack for t in ("audit", "fiscal", "tributário", "tributario")):
        return "fiscal"
    if "engenh" in haystack:
        return "engenharia"
    return None


class Parser(BaseParser):
    source_id: ClassVar[str] = "fgv"
    parser_version: ClassVar[str] = "1.0.0"

    def parse(self, snapshot: RawSnapshot) -> list[ParsedOpportunity]:
        tree = HTMLParser(snapshot.text)
        articles = tree.css("article.processo")
        results: list[ParsedOpportunity] = []

        for article in articles:
            title_node = article.css_first("h2.titulo a") or article.css_first("h2.titulo")
            title = _text(title_node)
            if not title or title_node is None:
                continue

            link: str | None = None
            if title_node.tag == "a":
                link = title_node.attributes.get("href")
            if link is None:
                anchor = article.css_first("h2.titulo a")
                link = anchor.attributes.get("href") if anchor else None
            detail_url = urljoin(snapshot.url, link) if link else snapshot.url

            kv = _parse_kv(article)
            organization = kv.get("órgão") or kv.get("orgao") or title
            position = kv.get("cargo")
            education = kv.get("escolaridade")
            salary_text = kv.get("remuneração") or kv.get("remuneracao")
            vacancies_text = kv.get("vagas")
            local = kv.get("local")
            period = kv.get("período de inscrição") or kv.get("periodo de inscricao")

            salary_min: Decimal | None = None
            salary_max: Decimal | None = None
            if salary_text and (m := _SALARY_RE.search(salary_text)):
                salary_min = _to_decimal(m.group(1))
                salary_max = _to_decimal(m.group(2)) if m.group(2) else salary_min

            vacancies = int(vacancies_text) if vacancies_text and vacancies_text.isdigit() else None

            city, uf = _split_local(local)
            reg_start = reg_end = None
            if period and (m := _DATE_RANGE_RE.search(period)):
                reg_start = _parse_date(m.group(1))
                reg_end = _parse_date(m.group(2))

            results.append(
                ParsedOpportunity(
                    title=title,
                    organization=organization,
                    board="fgv",
                    area=_infer_area(title, position),
                    position_name=position,
                    education_level=education,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    vacancies=vacancies,
                    state=uf,
                    city=city,
                    status="open",
                    registration_start_date=reg_start,
                    registration_end_date=reg_end,
                    source_url=detail_url,
                    confidence_level="high",
                )
            )

        return results

"""PCI Concursos HTML parser — aggregator table format.

Layout assumptions (versioned via ``parser_version``):
- Rows are ``tr.concurso-row``.
- Columns, in order: Concurso (with anchor), Cargos, Salário, Vagas, UF, Inscrições.
- "Inscrições" may be a free-text label like "Previsto" when dates are unknown.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from decimal import Decimal
from typing import ClassVar, Literal
from urllib.parse import urljoin

from selectolax.parser import HTMLParser, Node

from crawlers.core.base import BaseParser
from crawlers.core.models import ParsedOpportunity, RawSnapshot

_SALARY_RE = re.compile(r"R\$\s*([\d.]+,\d{2})(?:\s*-\s*R\$\s*([\d.]+,\d{2}))?")
_DATE_RANGE_RE = re.compile(r"(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})")


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


def _parse_int(text: str | None) -> int | None:
    if not text:
        return None
    digits = "".join(ch for ch in text if ch.isdigit())
    return int(digits) if digits else None


def _split_title(text: str) -> tuple[str, str | None]:
    """Title is usually "Organização — Cargo/Detalhe"."""

    for sep in (" — ", " - ", " – "):
        if sep in text:
            org, rest = text.split(sep, 1)
            return rest.strip(), org.strip()
    return text, None


def _infer_area(title: str, position: str | None) -> str | None:
    haystack = f"{title} {position or ''}".lower()
    if any(t in haystack for t in ("procurador", "advogado", "jurídic", "juridic")):
        return "juridica"
    if any(t in haystack for t in ("audit", "fiscal", "tributário", "tributario")):
        return "fiscal"
    if any(t in haystack for t in ("legislativo", "administr")):
        return "administrativo"
    if any(t in haystack for t in ("sistema", "software", "tecnologia", "desenvolv")):
        return "tecnologia"
    if re.search(r"\bti\b", haystack):
        return "tecnologia"
    return None


class Parser(BaseParser):
    source_id: ClassVar[str] = "pci-concursos"
    parser_version: ClassVar[str] = "1.0.0"

    def parse(self, snapshot: RawSnapshot) -> list[ParsedOpportunity]:
        tree = HTMLParser(snapshot.text)
        rows = tree.css("tr.concurso-row")
        results: list[ParsedOpportunity] = []

        for row in rows:
            cells = row.css("td")
            if len(cells) < 6:
                continue

            anchor = cells[0].css_first("a")
            raw_title = _text(anchor) or _text(cells[0])
            if not raw_title:
                continue
            href = anchor.attributes.get("href") if anchor else None
            detail_url = urljoin(snapshot.url, href) if href else snapshot.url

            position = _text(cells[1])
            normalized_title, org_from_title = _split_title(raw_title)
            organization = org_from_title or raw_title
            display_title = raw_title  # keep the user-facing string verbatim

            salary_text = _text(cells[2])
            salary_min: Decimal | None = None
            salary_max: Decimal | None = None
            if salary_text and (m := _SALARY_RE.search(salary_text)):
                salary_min = _to_decimal(m.group(1))
                salary_max = _to_decimal(m.group(2)) if m.group(2) else salary_min

            vacancies = _parse_int(_text(cells[3]))
            uf = _text(cells[4])
            if uf and (len(uf) != 2 or not uf.isalpha()):
                uf = None

            inscricoes = _text(cells[5])
            reg_start = reg_end = None
            status: Literal["draft", "open", "closed", "cancelled"] = "open"
            if inscricoes:
                if m := _DATE_RANGE_RE.search(inscricoes):
                    reg_start = _parse_date(m.group(1))
                    reg_end = _parse_date(m.group(2))
                elif inscricoes.lower() in {"previsto", "a definir"}:
                    status = "draft"

            results.append(
                ParsedOpportunity(
                    title=display_title,
                    organization=organization,
                    board=None,
                    area=_infer_area(display_title, position),
                    position_name=position or normalized_title,
                    education_level=None,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    vacancies=vacancies,
                    state=uf,
                    status=status,
                    registration_start_date=reg_start,
                    registration_end_date=reg_end,
                    source_url=detail_url,
                    confidence_level="medium",
                )
            )

        return results

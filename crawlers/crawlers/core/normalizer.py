"""Normalize ParsedOpportunity into canonical form.

Handles common cleanups:
- area name canonicalization (lowercase, slug-ish)
- state code uppercase
- city case
- education level mapping
- removes duplicate keywords, lowercases
"""

from __future__ import annotations

import re
from datetime import date
from decimal import Decimal

from crawlers.core.models import ParsedOpportunity

_AREA_SYNONYMS = {
    "ti": "tecnologia",
    "tecnologia da informação": "tecnologia",
    "tecnologia da informacao": "tecnologia",
    "sistemas": "tecnologia",
    "informática": "tecnologia",
    "informatica": "tecnologia",
    "juridico": "juridica",
    "direito": "juridica",
    "administração": "administrativo",
    "administracao": "administrativo",
    "saúde": "saude",
    "engenharia": "engenharia",
    "fiscal": "fiscal",
    "tributário": "fiscal",
    "tributario": "fiscal",
    "auditoria": "fiscal",
    "segurança pública": "seguranca_publica",
    "seguranca publica": "seguranca_publica",
    "policia": "seguranca_publica",
}

_EDUCATION_MAP = {
    "fundamental": "fundamental",
    "ensino fundamental": "fundamental",
    "médio": "medio",
    "medio": "medio",
    "ensino médio": "medio",
    "técnico": "tecnico",
    "tecnico": "tecnico",
    "superior": "superior",
    "ensino superior": "superior",
    "graduação": "superior",
    "graduacao": "superior",
    "pós-graduação": "pos_graduacao",
    "pos-graduacao": "pos_graduacao",
    "pós graduação": "pos_graduacao",
    "pos graduacao": "pos_graduacao",
    "mestrado": "pos_graduacao",
    "doutorado": "pos_graduacao",
}


class Normalizer:
    """Pure-functional normalizer over ParsedOpportunity."""

    @staticmethod
    def normalize(parsed: ParsedOpportunity) -> ParsedOpportunity:
        data = parsed.model_dump()
        data["area"] = _normalize_area(data.get("area"))
        data["state"] = _normalize_state(data.get("state"))
        data["city"] = _normalize_city(data.get("city"))
        data["education_level"] = _normalize_education(data.get("education_level"))
        data["title"] = _strip(data["title"])
        data["organization"] = _strip(data["organization"])
        data["position_name"] = _strip(data.get("position_name"))
        data["description"] = _strip(data.get("description"))
        data["board"] = _normalize_simple(data.get("board"))
        data["keywords"] = _normalize_keywords(data.get("keywords"))
        data["salary_min"] = _coerce_decimal(data.get("salary_min"))
        data["salary_max"] = _coerce_decimal(data.get("salary_max"))
        data["status"] = _infer_status(data)
        return ParsedOpportunity.model_validate(data)


def _strip(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = " ".join(value.split())
        return cleaned or None
    return str(value)


def _normalize_area(value: object) -> str | None:
    if not value or not isinstance(value, str):
        return None
    lowered = value.strip().lower()
    return _AREA_SYNONYMS.get(lowered, lowered)


def _normalize_state(value: object) -> str | None:
    if not value or not isinstance(value, str):
        return None
    candidate = value.strip().upper()
    if len(candidate) != 2 or not candidate.isalpha():
        return None
    return candidate


def _normalize_city(value: object) -> str | None:
    if not value or not isinstance(value, str):
        return None
    return value.strip().title()


def _normalize_education(value: object) -> str | None:
    if not value or not isinstance(value, str):
        return None
    return _EDUCATION_MAP.get(value.strip().lower())


def _normalize_simple(value: object) -> str | None:
    if not value or not isinstance(value, str):
        return None
    return value.strip().lower()


def _normalize_keywords(value: object) -> list[str] | None:
    if not value or not isinstance(value, list):
        return None
    seen: list[str] = []
    for raw in value:
        if not isinstance(raw, str):
            continue
        cleaned = raw.strip().lower()
        if cleaned and cleaned not in seen:
            seen.append(cleaned)
    return seen or None


def _coerce_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        cleaned = re.sub(r"[^\d,.\-]", "", value).replace(".", "").replace(",", ".")
        try:
            return Decimal(cleaned) if cleaned else None
        except (ValueError, ArithmeticError):
            return None
    return None


def _infer_status(data: dict[str, object]) -> str:
    today = date.today()
    start = data.get("registration_start_date")
    end = data.get("registration_end_date")
    explicit = data.get("status")

    if explicit and explicit != "draft":
        return str(explicit)

    if isinstance(end, date) and end < today:
        return "closed"
    if isinstance(start, date) and start <= today:
        return "open"
    if isinstance(start, date):
        return "draft"
    return "open" if isinstance(end, date) and end >= today else "draft"

"""Deterministic parser tests against versioned HTML fixtures."""

from __future__ import annotations

import hashlib
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from crawlers.core.models import RawSnapshot
from crawlers.sources.cebraspe.parser import Parser

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def _snapshot(filename: str) -> RawSnapshot:
    content = (FIXTURES / filename).read_bytes()
    return RawSnapshot(
        source_id="cebraspe",
        url=f"https://www.cebraspe.org.br/{filename}",
        content=content,
        content_type="text/html",
        content_hash=hashlib.sha256(content).hexdigest(),
    )


class TestConcursosAbertosFixture:
    @pytest.fixture
    def parsed(self) -> list:
        return Parser().parse(_snapshot("concursos_abertos.html"))

    def test_returns_three_items(self, parsed: list) -> None:
        assert len(parsed) == 3

    def test_first_item_is_trf1(self, parsed: list) -> None:
        first = parsed[0]
        assert first.title.startswith("TRF 1ª Região")
        assert first.organization == "Tribunal Regional Federal da 1ª Região"
        assert first.position_name == "Analista Judiciário — Análise de Sistemas"
        assert first.state == "DF"
        assert first.vacancies == 30
        assert first.salary_min == Decimal("13994.78")
        assert first.salary_max == Decimal("13994.78")
        assert first.registration_start_date == date(2026, 5, 15)
        assert first.registration_end_date == date(2026, 6, 30)
        assert first.status == "open"
        assert first.area == "tecnologia"
        assert first.confidence_level == "high"

    def test_pf_item_area_inferred(self, parsed: list) -> None:
        pf = parsed[1]
        assert pf.title.startswith("Polícia Federal")
        assert pf.area == "seguranca_publica"
        assert pf.vacancies == 700

    def test_salary_range_when_provided(self, parsed: list) -> None:
        ms = parsed[2]
        assert ms.salary_min == Decimal("9000.00")
        assert ms.salary_max == Decimal("12000.00")

    def test_source_url_absolute(self, parsed: list) -> None:
        assert parsed[0].source_url.startswith("https://www.cebraspe.org.br/")

    def test_deterministic(self) -> None:
        a = Parser().parse(_snapshot("concursos_abertos.html"))
        b = Parser().parse(_snapshot("concursos_abertos.html"))
        assert [o.title for o in a] == [o.title for o in b]
        assert [o.salary_max for o in a] == [o.salary_max for o in b]


class TestConcursoEncerradoFixture:
    def test_parses_closed_contest(self) -> None:
        parsed = Parser().parse(_snapshot("concurso_encerrado.html"))
        assert len(parsed) == 1
        opp = parsed[0]
        assert opp.title.startswith("Receita Federal")
        assert opp.area == "fiscal"
        assert opp.registration_end_date == date(2026, 3, 10)
        # The parser tags status=open by default; Normalizer later infers
        # `closed` because registration_end is in the past.
        assert opp.status == "open"


class TestSemSalarioFixture:
    def test_missing_salary_handled_gracefully(self) -> None:
        parsed = Parser().parse(_snapshot("sem_salario.html"))
        assert len(parsed) == 1
        opp = parsed[0]
        assert opp.salary_min is None
        assert opp.salary_max is None
        assert opp.vacancies == 12
        assert opp.state == "SP"


class TestEmptyFixture:
    def test_empty_returns_empty(self) -> None:
        snap = RawSnapshot(
            source_id="cebraspe",
            url="https://example.com/empty",
            content=b"<html><body></body></html>",
            content_type="text/html",
            content_hash="x",
        )
        assert Parser().parse(snap) == []


class TestVersioning:
    def test_parser_declares_version(self) -> None:
        assert Parser.parser_version == "1.0.0"
        assert Parser.source_id == "cebraspe"

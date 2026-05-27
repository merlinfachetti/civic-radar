"""FGV parser tests against versioned HTML fixtures."""

from __future__ import annotations

import hashlib
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from crawlers.core.models import RawSnapshot
from crawlers.sources.fgv.parser import Parser

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def _snapshot(filename: str) -> RawSnapshot:
    content = (FIXTURES / filename).read_bytes()
    return RawSnapshot(
        source_id="fgv",
        url=f"https://conhecimento.fgv.br/{filename}",
        content=content,
        content_type="text/html",
        content_hash=hashlib.sha256(content).hexdigest(),
    )


class TestIndexFixture:
    @pytest.fixture
    def parsed(self) -> list:
        return Parser().parse(_snapshot("index.html"))

    def test_three_items(self, parsed: list) -> None:
        assert len(parsed) == 3

    def test_tjsp_parsed(self, parsed: list) -> None:
        tjsp = parsed[0]
        assert tjsp.title.startswith("Tribunal de Justiça SP")
        assert tjsp.organization == "Tribunal de Justiça do Estado de São Paulo"
        assert tjsp.state == "SP"
        assert tjsp.city == "São Paulo"
        assert tjsp.area == "tecnologia"
        assert tjsp.salary_min == Decimal("11500.50")
        assert tjsp.salary_max == Decimal("14250.00")
        assert tjsp.vacancies == 45
        assert tjsp.registration_start_date == date(2026, 5, 25)
        assert tjsp.registration_end_date == date(2026, 7, 15)

    def test_bcb_single_salary(self, parsed: list) -> None:
        bcb = parsed[1]
        assert bcb.salary_min == Decimal("20925.00")
        assert bcb.salary_max == Decimal("20925.00")
        assert bcb.area == "tecnologia"

    def test_petrobras_engineering_area(self, parsed: list) -> None:
        petro = parsed[2]
        assert petro.area in {"engenharia", "tecnologia"}
        assert petro.state == "RJ"


class TestRegionalFixture:
    def test_medical_area_inferred(self) -> None:
        parsed = Parser().parse(_snapshot("regional.html"))
        assert len(parsed) == 1
        opp = parsed[0]
        assert opp.area == "saude"
        assert opp.city == "Niterói"
        assert opp.state == "RJ"


class TestEmptyFixture:
    def test_no_articles_returns_empty(self) -> None:
        assert Parser().parse(_snapshot("empty.html")) == []


class TestVersioning:
    def test_version_and_id(self) -> None:
        assert Parser.parser_version == "1.0.0"
        assert Parser.source_id == "fgv"

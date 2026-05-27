"""PCI Concursos parser tests against versioned HTML fixtures."""

from __future__ import annotations

import hashlib
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from crawlers.core.models import RawSnapshot
from crawlers.sources.pci_concursos.parser import Parser

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def _snapshot(filename: str) -> RawSnapshot:
    content = (FIXTURES / filename).read_bytes()
    return RawSnapshot(
        source_id="pci-concursos",
        url=f"https://www.pciconcursos.com.br/{filename}",
        content=content,
        content_type="text/html",
        content_hash=hashlib.sha256(content).hexdigest(),
    )


class TestAbertosFixture:
    @pytest.fixture
    def parsed(self) -> list:
        return Parser().parse(_snapshot("abertos.html"))

    def test_three_rows_parsed(self, parsed: list) -> None:
        assert len(parsed) == 3

    def test_procurador_curitiba(self, parsed: list) -> None:
        first = parsed[0]
        assert "Curitiba" in first.title
        assert first.area == "juridica"
        assert first.state == "PR"
        assert first.salary_min == Decimal("18500.00")
        assert first.salary_max == Decimal("24000.00")
        assert first.vacancies == 12
        assert first.registration_end_date == date(2026, 6, 25)
        assert first.confidence_level == "medium"

    def test_auditor_rio_fiscal_area(self, parsed: list) -> None:
        auditor = parsed[1]
        assert auditor.area == "fiscal"
        assert auditor.state == "RJ"

    def test_tecnico_legislativo_area(self, parsed: list) -> None:
        tecnico = parsed[2]
        assert tecnico.area == "administrativo"
        assert tecnico.state == "MG"
        assert tecnico.vacancies == 35


class TestSemInscricoesFixture:
    def test_previsto_marks_status_draft(self) -> None:
        parsed = Parser().parse(_snapshot("sem_inscricoes.html"))
        assert len(parsed) == 1
        opp = parsed[0]
        assert opp.status == "draft"
        assert opp.registration_start_date is None
        assert opp.registration_end_date is None
        assert opp.state == "MS"


class TestEncerradoFixture:
    def test_parses_vacancies_with_thousand_separator(self) -> None:
        parsed = Parser().parse(_snapshot("encerrado.html"))
        assert len(parsed) == 1
        opp = parsed[0]
        # "1.000" → 1000
        assert opp.vacancies == 1000
        # The parser accepts any 2-letter alpha as a UF candidate.
        # Real UF validation lives in the Normalizer.
        assert opp.state == "BR"


class TestVersioning:
    def test_version_and_id(self) -> None:
        assert Parser.parser_version == "1.0.0"
        assert Parser.source_id == "pci-concursos"

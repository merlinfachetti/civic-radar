"""Tests for the canonical normalizer."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from crawlers.core.models import ParsedOpportunity
from crawlers.core.normalizer import Normalizer


def _make(**overrides: object) -> ParsedOpportunity:
    base: dict[str, object] = {
        "title": " Some  Title ",
        "organization": " Org X ",
        "source_url": "https://example.com/x",
        "status": "draft",
    }
    base.update(overrides)
    return ParsedOpportunity.model_validate(base)


class TestStringNormalization:
    def test_title_whitespace_collapsed(self) -> None:
        result = Normalizer.normalize(_make(title="   foo    bar  "))
        assert result.title == "foo bar"

    def test_state_uppercased(self) -> None:
        result = Normalizer.normalize(_make(state="sp"))
        assert result.state == "SP"

    def test_invalid_state_dropped(self) -> None:
        result = Normalizer.normalize(_make(state="ZZ123"))
        assert result.state is None

    def test_city_title_cased(self) -> None:
        result = Normalizer.normalize(_make(city="são paulo"))
        assert result.city == "São Paulo"


class TestAreaSynonyms:
    def test_ti_maps_to_tecnologia(self) -> None:
        assert Normalizer.normalize(_make(area="ti")).area == "tecnologia"

    def test_direito_maps_to_juridica(self) -> None:
        assert Normalizer.normalize(_make(area="direito")).area == "juridica"

    def test_unknown_area_lowercased(self) -> None:
        assert Normalizer.normalize(_make(area="Foo")).area == "foo"

    def test_none_area_stays_none(self) -> None:
        assert Normalizer.normalize(_make(area=None)).area is None


class TestEducationLevel:
    def test_medio_normalized(self) -> None:
        assert Normalizer.normalize(_make(education_level="Médio")).education_level == "medio"

    def test_pos_graduacao_variants(self) -> None:
        for variant in ("Pós-Graduação", "pos graduacao", "Mestrado"):
            assert (
                Normalizer.normalize(_make(education_level=variant)).education_level
                == "pos_graduacao"
            )


class TestKeywordsDedup:
    def test_keywords_deduped_lowercased(self) -> None:
        result = Normalizer.normalize(_make(keywords=["Foo", "FOO", "bar", "  bar "]))
        assert result.keywords == ["foo", "bar"]

    def test_empty_keywords_becomes_none(self) -> None:
        assert Normalizer.normalize(_make(keywords=[])).keywords is None


class TestStatusInference:
    def test_future_registration_opens(self) -> None:
        end = date.today() + timedelta(days=30)
        result = Normalizer.normalize(_make(registration_end_date=end, status="draft"))
        assert result.status == "open"

    def test_past_registration_closes(self) -> None:
        end = date.today() - timedelta(days=10)
        result = Normalizer.normalize(_make(registration_end_date=end, status="draft"))
        assert result.status == "closed"

    def test_explicit_status_preserved(self) -> None:
        result = Normalizer.normalize(_make(status="cancelled"))
        assert result.status == "cancelled"


class TestSalaryCoercion:
    def test_decimal_preserved(self) -> None:
        result = Normalizer.normalize(_make(salary_min=Decimal("123.45")))
        assert result.salary_min == Decimal("123.45")

    def test_none_stays_none(self) -> None:
        result = Normalizer.normalize(_make(salary_min=None))
        assert result.salary_min is None

"""Unit tests for Pydantic schemas (normalization, validation)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from civic_radar.db.models import EducationLevel
from civic_radar.schemas.match import MatchProfile


class TestMatchProfileNormalization:
    def test_states_uppercased(self) -> None:
        profile = MatchProfile(states=["sp", "rj"])
        assert profile.states == ["SP", "RJ"]

    def test_areas_lowercased_and_stripped(self) -> None:
        profile = MatchProfile(areas=["  TECNOLOGIA ", "Juridica"])
        assert profile.areas == ["tecnologia", "juridica"]

    def test_keywords_normalized(self) -> None:
        profile = MatchProfile(keywords=["  Analista de Sistemas ", "DESENVOLVEDOR"])
        assert profile.keywords == ["analista de sistemas", "desenvolvedor"]

    def test_empty_strings_filtered_out(self) -> None:
        profile = MatchProfile(areas=["", "   ", "valid"])
        assert profile.areas == ["valid"]

    def test_minimum_salary_must_be_non_negative(self) -> None:
        with pytest.raises(ValidationError):
            MatchProfile(minimum_salary=-1)

    def test_education_level_validates(self) -> None:
        profile = MatchProfile(education_level=EducationLevel.SUPERIOR)
        assert profile.education_level == EducationLevel.SUPERIOR

    def test_default_empty_lists(self) -> None:
        profile = MatchProfile()
        assert profile.areas == []
        assert profile.states == []
        assert profile.keywords == []
        assert profile.minimum_salary is None

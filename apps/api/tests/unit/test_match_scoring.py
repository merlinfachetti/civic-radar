"""Unit tests for the deterministic match scoring engine."""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

import pytest

from civic_radar.db.models import (
    EducationLevel,
    Opportunity,
    OpportunityStatus,
)
from civic_radar.match.scoring import WEIGHTS, score_opportunity
from civic_radar.schemas.match import MatchProfile


def _make_opportunity(**overrides: object) -> Opportunity:
    base: dict[str, object] = {
        "id": "opp-1",
        "title": "Analista de Sistemas",
        "organization": "Órgão Federal",
        "board": "cebraspe",
        "area": "tecnologia",
        "position_name": "Analista de Sistemas",
        "education_level": EducationLevel.SUPERIOR,
        "salary_min": Decimal("8000.00"),
        "salary_max": Decimal("12000.00"),
        "state": "SP",
        "city": "São Paulo",
        "status": OpportunityStatus.OPEN,
        "source_url": "https://example.com/x",
        "registration_end_date": date.today() + timedelta(days=20),
    }
    base.update(overrides)
    return Opportunity(**base)


class TestPerfectMatch:
    def test_full_score_when_everything_aligns(self) -> None:
        profile = MatchProfile(
            areas=["tecnologia"],
            states=["SP"],
            education_level=EducationLevel.SUPERIOR,
            minimum_salary=6000,
            keywords=["analista"],
        )
        opp = _make_opportunity()
        result = score_opportunity(profile, opp)
        assert result.score == 100
        assert all(r.points > 0 for r in result.reasons[:5])

    def test_empty_profile_yields_status_only(self) -> None:
        profile = MatchProfile()
        opp = _make_opportunity()
        result = score_opportunity(profile, opp)
        assert 0 < result.score <= WEIGHTS["status"]


class TestAreaScore:
    def test_area_match_full_points(self) -> None:
        profile = MatchProfile(areas=["tecnologia"])
        opp = _make_opportunity(area="tecnologia")
        result = score_opportunity(profile, opp)
        assert _points_for(result, "area") == WEIGHTS["area"]

    def test_area_mismatch_zero(self) -> None:
        profile = MatchProfile(areas=["juridica"])
        opp = _make_opportunity(area="tecnologia")
        assert _points_for(score_opportunity(profile, opp), "area") == 0

    def test_area_none_yields_zero(self) -> None:
        profile = MatchProfile(areas=["tecnologia"])
        opp = _make_opportunity(area=None)
        assert _points_for(score_opportunity(profile, opp), "area") == 0


class TestKeywordScore:
    def test_full_keyword_match(self) -> None:
        profile = MatchProfile(keywords=["analista"])
        opp = _make_opportunity(title="Concurso de Analista de Sistemas")
        result = score_opportunity(profile, opp)
        assert _points_for(result, "keyword") == WEIGHTS["keyword"]

    def test_partial_keyword_match_is_proportional(self) -> None:
        profile = MatchProfile(keywords=["analista", "ausente"])
        opp = _make_opportunity(title="Analista de Sistemas")
        result = score_opportunity(profile, opp)
        assert _points_for(result, "keyword") == WEIGHTS["keyword"] // 2

    def test_case_insensitive(self) -> None:
        profile = MatchProfile(keywords=["ANALISTA"])
        opp = _make_opportunity(title="analista de sistemas")
        result = score_opportunity(profile, opp)
        assert _points_for(result, "keyword") == WEIGHTS["keyword"]


class TestLocationScore:
    def test_state_match(self) -> None:
        profile = MatchProfile(states=["SP"])
        opp = _make_opportunity(state="SP")
        assert _points_for(score_opportunity(profile, opp), "location") == WEIGHTS["location"]

    def test_state_mismatch(self) -> None:
        profile = MatchProfile(states=["RJ"])
        opp = _make_opportunity(state="SP")
        assert _points_for(score_opportunity(profile, opp), "location") == 0

    def test_state_normalized_lower_to_upper(self) -> None:
        profile = MatchProfile(states=["sp"])
        opp = _make_opportunity(state="SP")
        assert _points_for(score_opportunity(profile, opp), "location") == WEIGHTS["location"]


class TestEducationScore:
    def test_higher_profile_education_matches(self) -> None:
        profile = MatchProfile(education_level=EducationLevel.POS_GRADUACAO)
        opp = _make_opportunity(education_level=EducationLevel.SUPERIOR)
        assert _points_for(score_opportunity(profile, opp), "education") == WEIGHTS["education"]

    def test_lower_profile_education_zero(self) -> None:
        profile = MatchProfile(education_level=EducationLevel.MEDIO)
        opp = _make_opportunity(education_level=EducationLevel.SUPERIOR)
        assert _points_for(score_opportunity(profile, opp), "education") == 0


class TestSalaryScore:
    def test_above_minimum_full_points(self) -> None:
        profile = MatchProfile(minimum_salary=5000)
        opp = _make_opportunity(salary_max=Decimal("10000"))
        assert _points_for(score_opportunity(profile, opp), "salary") == WEIGHTS["salary"]

    def test_below_minimum_zero(self) -> None:
        profile = MatchProfile(minimum_salary=20000)
        opp = _make_opportunity(salary_max=Decimal("10000"))
        assert _points_for(score_opportunity(profile, opp), "salary") == 0

    def test_no_salary_in_profile_zero(self) -> None:
        profile = MatchProfile()
        opp = _make_opportunity()
        assert _points_for(score_opportunity(profile, opp), "salary") == 0


class TestStatusScore:
    def test_open_far_future_full_points(self) -> None:
        opp = _make_opportunity(registration_end_date=date.today() + timedelta(days=60))
        assert _points_for(score_opportunity(MatchProfile(), opp), "status") == WEIGHTS["status"]

    def test_open_close_to_deadline_half_points(self) -> None:
        opp = _make_opportunity(registration_end_date=date.today() + timedelta(days=2))
        assert (
            _points_for(score_opportunity(MatchProfile(), opp), "status") == WEIGHTS["status"] // 2
        )

    def test_closed_zero(self) -> None:
        opp = _make_opportunity(status=OpportunityStatus.CLOSED)
        assert _points_for(score_opportunity(MatchProfile(), opp), "status") == 0


class TestDeterminism:
    def test_same_input_same_output(self) -> None:
        profile = MatchProfile(areas=["tecnologia"], states=["SP"], minimum_salary=6000)
        opp = _make_opportunity()
        a = score_opportunity(profile, opp)
        b = score_opportunity(profile, opp)
        assert a.score == b.score
        assert [r.points for r in a.reasons] == [r.points for r in b.reasons]


def _points_for(result: object, criterion: str) -> int:
    for reason in result.reasons:  # type: ignore[attr-defined]
        if reason.criterion == criterion:
            return reason.points
    pytest.fail(f"criterion {criterion} not in reasons")
    return 0

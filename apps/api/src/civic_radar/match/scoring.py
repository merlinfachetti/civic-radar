"""Deterministic, explainable match scoring.

Weights are derived from PRODUCT_FOUNDATION §15:

    Area match        30
    Keyword match     20
    Location match    15
    Education level   15
    Salary match      10
    Status/date       10
    ────────────────────
    Total            100
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date, timedelta

from civic_radar.db.models import Opportunity, OpportunityStatus
from civic_radar.schemas.match import MatchProfile, MatchReason

WEIGHTS: dict[str, int] = {
    "area": 30,
    "keyword": 20,
    "location": 15,
    "education": 15,
    "salary": 10,
    "status": 10,
}

MAX_SCORE: int = sum(WEIGHTS.values())


@dataclass(frozen=True)
class MatchScore:
    opportunity_id: str
    score: int
    reasons: list[MatchReason] = field(default_factory=list)


def _score_area(profile: MatchProfile, opp: Opportunity) -> tuple[int, str]:
    weight = WEIGHTS["area"]
    if not profile.areas:
        return 0, "Sem áreas no perfil"
    if not opp.area:
        return 0, "Oportunidade sem área classificada"
    if opp.area.lower() in profile.areas:
        return weight, f"Área '{opp.area}' compatível com perfil"
    return 0, f"Área '{opp.area}' não está no perfil"


def _score_keyword(profile: MatchProfile, opp: Opportunity) -> tuple[int, str]:
    weight = WEIGHTS["keyword"]
    if not profile.keywords:
        return 0, "Sem palavras-chave no perfil"

    haystacks: list[str] = []
    for value in (opp.title, opp.position_name, opp.description, opp.organization):
        if value:
            haystacks.append(value.lower())
    if not haystacks:
        return 0, "Oportunidade sem texto pesquisável"

    matched = [kw for kw in profile.keywords if any(kw in h for h in haystacks)]
    if not matched:
        return 0, "Nenhuma palavra-chave do perfil encontrada"

    ratio = len(matched) / len(profile.keywords)
    points = round(weight * ratio)
    return points, f"Match em palavra(s)-chave: {', '.join(matched)}"


def _score_location(profile: MatchProfile, opp: Opportunity) -> tuple[int, str]:
    weight = WEIGHTS["location"]
    if not profile.states and not profile.cities:
        return 0, "Sem localização no perfil"

    if opp.state and opp.state in profile.states:
        if opp.city and profile.cities and opp.city.lower() in {c.lower() for c in profile.cities}:
            return weight, f"Cidade {opp.city}/{opp.state} está no perfil"
        return weight, f"Estado {opp.state} está no perfil"
    if opp.city and opp.city.lower() in {c.lower() for c in profile.cities}:
        return weight, f"Cidade {opp.city} está no perfil"

    return 0, f"Localização {opp.city or '?'}/{opp.state or '?'} não está no perfil"


_EDUCATION_RANK: dict[str, int] = {
    "fundamental": 1,
    "medio": 2,
    "tecnico": 3,
    "superior": 4,
    "pos_graduacao": 5,
}


def _score_education(profile: MatchProfile, opp: Opportunity) -> tuple[int, str]:
    weight = WEIGHTS["education"]
    if not profile.education_level or not opp.education_level:
        return 0, "Escolaridade não comparável (faltando perfil ou oportunidade)"

    p_rank = _EDUCATION_RANK[profile.education_level.value]
    o_rank = _EDUCATION_RANK[opp.education_level.value]

    if p_rank >= o_rank:
        return weight, (
            f"Escolaridade '{opp.education_level.value}' compatível com perfil "
            f"'{profile.education_level.value}'"
        )
    return 0, (
        f"Escolaridade '{opp.education_level.value}' acima do perfil "
        f"'{profile.education_level.value}'"
    )


def _score_salary(profile: MatchProfile, opp: Opportunity) -> tuple[int, str]:
    weight = WEIGHTS["salary"]
    if profile.minimum_salary is None:
        return 0, "Sem salário mínimo no perfil"

    candidate_salary = opp.salary_max or opp.salary_min
    if candidate_salary is None:
        return 0, "Oportunidade sem salário declarado"

    if float(candidate_salary) >= profile.minimum_salary:
        return weight, (
            f"Salário R$ {opp.salary_min or 0:.2f}–{candidate_salary:.2f} "
            f"acima do mínimo R$ {profile.minimum_salary:.2f}"
        )
    return 0, (
        f"Salário R$ {candidate_salary:.2f} abaixo do mínimo R$ {profile.minimum_salary:.2f}"
    )


def _score_status(opp: Opportunity, today: date | None = None) -> tuple[int, str]:
    weight = WEIGHTS["status"]
    today = today or date.today()

    if opp.status != OpportunityStatus.OPEN:
        return 0, f"Status '{opp.status.value}' não está aberto"

    if not opp.registration_end_date:
        return weight, "Inscrições abertas (sem data de fim)"

    delta = (opp.registration_end_date - today).days
    if delta < 0:
        return 0, "Inscrições já encerradas (data passada)"
    if delta <= 3:
        return weight // 2, (f"Inscrições encerram em {delta} dia(s) — atenção ao prazo")
    if delta <= 14:
        return weight, f"Inscrições abertas, encerram em {delta} dias"
    return weight, f"Inscrições abertas com {delta} dias de antecedência"


def score_opportunity(
    profile: MatchProfile,
    opp: Opportunity,
    today: date | None = None,
) -> MatchScore:
    """Compute the match score for a single opportunity against a profile."""

    reasons: list[MatchReason] = []
    total = 0

    scorers: tuple[tuple[str, Callable[[], tuple[int, str]]], ...] = (
        ("area", lambda: _score_area(profile, opp)),
        ("keyword", lambda: _score_keyword(profile, opp)),
        ("location", lambda: _score_location(profile, opp)),
        ("education", lambda: _score_education(profile, opp)),
        ("salary", lambda: _score_salary(profile, opp)),
        ("status", lambda: _score_status(opp, today)),
    )
    for criterion, scorer in scorers:
        points, explanation = scorer()
        total += points
        reasons.append(
            MatchReason(
                criterion=criterion,
                points=points,
                weight=WEIGHTS[criterion],
                explanation=explanation,
            )
        )

    return MatchScore(opportunity_id=opp.id, score=total, reasons=reasons)


def freshness_bonus_days() -> int:
    """Public helper for explainability UI."""

    return (date.today() + timedelta(days=14)).toordinal() - date.today().toordinal()

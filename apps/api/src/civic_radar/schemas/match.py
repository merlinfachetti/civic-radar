"""Pydantic schemas for the match endpoint."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from civic_radar.db.models import EducationLevel
from civic_radar.schemas.opportunity import OpportunityRead


class MatchProfile(BaseModel):
    """User-supplied profile to compute match scores against opportunities.

    All fields are optional; a fully-empty profile yields neutral scores
    (mostly status-based).
    """

    areas: list[str] = Field(default_factory=list, max_length=20)
    states: list[str] = Field(default_factory=list, max_length=27, description="2-letter UF codes")
    cities: list[str] = Field(default_factory=list, max_length=50)
    education_level: EducationLevel | None = None
    minimum_salary: float | None = Field(default=None, ge=0)
    keywords: list[str] = Field(default_factory=list, max_length=30)
    include_remote: bool = False

    @field_validator("states")
    @classmethod
    def states_uppercase(cls, value: list[str]) -> list[str]:
        return [v.upper() for v in value]

    @field_validator("areas", "keywords")
    @classmethod
    def lowercase_strip(cls, value: list[str]) -> list[str]:
        return [v.strip().lower() for v in value if v.strip()]


class MatchReason(BaseModel):
    criterion: str
    points: int
    weight: int
    explanation: str


class MatchResult(BaseModel):
    opportunity_id: str
    opportunity: OpportunityRead
    score: int = Field(..., ge=0, le=100)
    max_score: int = 100
    reasons: list[MatchReason]


class MatchResponse(BaseModel):
    matches: list[MatchResult]
    total_evaluated: int
    total_returned: int

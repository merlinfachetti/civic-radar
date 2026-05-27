"""Pydantic schemas for the public stats endpoint."""

from __future__ import annotations

from pydantic import BaseModel


class StatsLast7Days(BaseModel):
    new_opportunities: int = 0
    closed_opportunities: int = 0


class SourcesStats(BaseModel):
    total: int = 0
    healthy: int = 0


class StatsResponse(BaseModel):
    total_opportunities: int
    open_opportunities: int
    closed_opportunities: int
    by_state: dict[str, int]
    by_area: dict[str, int]
    by_education_level: dict[str, int]
    last_7_days: StatsLast7Days
    sources: SourcesStats

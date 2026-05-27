"""Pydantic schemas for opportunity endpoints."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from civic_radar.db.models import (
    ConfidenceLevel,
    EducationLevel,
    OpportunityStatus,
)


class OpportunityRead(BaseModel):
    """Compact opportunity representation for list endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: str = Field(..., description="UUID")
    title: str
    organization: str
    board: str | None = None
    area: str | None = None
    position_name: str | None = None
    education_level: EducationLevel | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    vacancies: int | None = None
    state: str | None = None
    city: str | None = None
    status: OpportunityStatus
    registration_start_date: date | None = None
    registration_end_date: date | None = None
    exam_date: date | None = None
    source_url: str
    confidence_level: ConfidenceLevel
    last_checked_at: datetime


class OpportunityDetailRead(OpportunityRead):
    """Full opportunity payload with description and audit metadata."""

    description: str | None = None
    original_url: str | None = None
    keywords: list[str] | None = None
    created_at: datetime
    updated_at: datetime


class PaginationMeta(BaseModel):
    next_cursor: str | None = Field(
        default=None,
        description="Opaque cursor for the next page. `null` when last page reached.",
    )
    has_more: bool = False
    total_count: int = Field(..., description="Total matching the filters")


class OpportunityListResponse(BaseModel):
    items: list[OpportunityRead]
    pagination: PaginationMeta

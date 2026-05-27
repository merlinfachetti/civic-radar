"""Pydantic schemas for source endpoints."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from civic_radar.db.models import ConfidenceLevel, SourceType


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_id: str
    name: str
    type: SourceType
    base_url: str
    quality_level: ConfidenceLevel
    enabled: bool
    last_successful_check_at: datetime | None = None
    items_count: int = 0


class SourceListResponse(BaseModel):
    items: list[SourceRead]

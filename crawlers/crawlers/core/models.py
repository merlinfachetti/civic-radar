"""Shared data containers across all crawlers and parsers."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RawSnapshot(BaseModel):
    """A captured page (HTML / PDF / JSON) ready to be parsed."""

    source_id: str
    url: str
    content: bytes
    content_type: str = "text/html"
    content_hash: str
    captured_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    parser_version: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def text(self) -> str:
        """Decode content as UTF-8 text. Use only for HTML/text snapshots."""

        return self.content.decode("utf-8", errors="replace")


class ParsedOpportunity(BaseModel):
    """A parsed opportunity, pre-normalization.

    Fields mirror the `Opportunity` ORM model but use plain types — the
    `Normalizer` is responsible for ORM-friendly conversions.
    """

    title: str
    description: str | None = None
    organization: str
    board: str | None = None
    area: str | None = None
    position_name: str | None = None
    education_level: str | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    vacancies: int | None = None
    state: str | None = None
    city: str | None = None
    status: Literal["draft", "open", "closed", "cancelled"] = "draft"
    registration_start_date: date | None = None
    registration_end_date: date | None = None
    exam_date: date | None = None
    source_url: str
    original_url: str | None = None
    confidence_level: Literal["high", "medium", "low"] = "medium"
    keywords: list[str] | None = None


class SourceConfig(BaseModel):
    """The contents of `crawlers/sources/<id>/config.yaml`."""

    id: str
    name: str
    type: Literal["agency", "organizing_board", "portal", "aggregator"]
    base_url: str
    enabled: bool = True
    robots_policy_required: bool = True
    rate_limit_seconds: int = 10
    parser: str
    parser_version: str = "0.1.0"
    quality_level: Literal["high", "medium", "low"] = "medium"
    maintainer: str | None = None

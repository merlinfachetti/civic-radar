"""Pydantic schemas for API request/response bodies."""

from civic_radar.schemas.match import MatchProfile, MatchReason, MatchResponse, MatchResult
from civic_radar.schemas.opportunity import (
    OpportunityDetailRead,
    OpportunityListResponse,
    OpportunityRead,
    PaginationMeta,
)
from civic_radar.schemas.source import SourceListResponse, SourceRead
from civic_radar.schemas.stats import StatsResponse

__all__ = [
    "MatchProfile",
    "MatchReason",
    "MatchResponse",
    "MatchResult",
    "OpportunityDetailRead",
    "OpportunityListResponse",
    "OpportunityRead",
    "PaginationMeta",
    "SourceListResponse",
    "SourceRead",
    "StatsResponse",
]

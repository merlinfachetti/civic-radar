"""Protocol-based contracts for source plugins."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from crawlers.core.models import ParsedOpportunity, RawSnapshot


@runtime_checkable
class SourceCrawler(Protocol):
    """A source crawler fetches raw snapshots from a public source."""

    source_id: str
    rate_limit_seconds: int

    async def fetch_list(self) -> list[RawSnapshot]: ...
    async def fetch_detail(self, snapshot: RawSnapshot) -> RawSnapshot: ...


@runtime_checkable
class SourceParser(Protocol):
    """A source parser converts raw snapshots into ParsedOpportunity items.

    Implementations must be **deterministic** and **side-effect free**.
    """

    source_id: str
    parser_version: str

    def parse(self, snapshot: RawSnapshot) -> list[ParsedOpportunity]: ...

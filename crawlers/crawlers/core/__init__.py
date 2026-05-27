"""CivicRadar — crawler/parser plugin core.

Public API:
    BaseCrawler, BaseParser  — base classes with rate limit + robots.txt
    RawSnapshot, ParsedOpportunity  — data containers shared across plugins
    SourceCrawler, SourceParser  — Protocols (interface contracts)
    Normalizer  — converts ParsedOpportunity into canonical fields
    SourceRegistry  — auto-discovery + lookup of available sources
"""

from crawlers.core.base import BaseCrawler, BaseParser
from crawlers.core.models import (
    ParsedOpportunity,
    RawSnapshot,
    SourceConfig,
)
from crawlers.core.normalizer import Normalizer
from crawlers.core.protocols import SourceCrawler, SourceParser
from crawlers.core.registry import SourceRegistry

__all__ = [
    "BaseCrawler",
    "BaseParser",
    "Normalizer",
    "ParsedOpportunity",
    "RawSnapshot",
    "SourceConfig",
    "SourceCrawler",
    "SourceParser",
    "SourceRegistry",
]

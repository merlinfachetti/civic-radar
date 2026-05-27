"""Cebraspe HTTP crawler."""

from __future__ import annotations

from typing import ClassVar

from crawlers.core.base import BaseCrawler
from crawlers.core.models import RawSnapshot

INDEX_URL = "https://www.cebraspe.org.br/concursos/abertos"


class Crawler(BaseCrawler):
    source_id: ClassVar[str] = "cebraspe"
    rate_limit_seconds: ClassVar[int] = 10

    async def fetch_list(self) -> list[RawSnapshot]:
        snapshot = await self._snapshot(INDEX_URL)
        return [snapshot]

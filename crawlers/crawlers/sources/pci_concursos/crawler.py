"""PCI Concursos HTTP crawler."""

from __future__ import annotations

from typing import ClassVar

from crawlers.core.base import BaseCrawler
from crawlers.core.models import RawSnapshot

INDEX_URL = "https://www.pciconcursos.com.br/concursos/"


class Crawler(BaseCrawler):
    source_id: ClassVar[str] = "pci-concursos"
    rate_limit_seconds: ClassVar[int] = 15

    async def fetch_list(self) -> list[RawSnapshot]:
        return [await self._snapshot(INDEX_URL)]

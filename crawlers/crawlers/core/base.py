"""Base classes for crawlers and parsers.

Concrete subclasses live in `crawlers/sources/<source_id>/`.
"""

from __future__ import annotations

import asyncio
import hashlib
import time
from abc import ABC, abstractmethod
from typing import ClassVar

import httpx
import structlog
from protego import Protego

from crawlers.core.models import ParsedOpportunity, RawSnapshot

log = structlog.get_logger("crawlers.base")


class BaseCrawler(ABC):
    """Common behavior: rate-limited HTTP, robots.txt enforcement, snapshotting."""

    source_id: ClassVar[str]
    rate_limit_seconds: ClassVar[int] = 10
    user_agent: ClassVar[str] = "CivicRadar/0.1 (+https://github.com/merlinfachetti/civic-radar)"

    def __init__(self, *, http_client: httpx.AsyncClient | None = None) -> None:
        self._client = http_client or httpx.AsyncClient(
            headers={"User-Agent": self.user_agent},
            follow_redirects=True,
            timeout=30.0,
        )
        self._last_request_at: float = 0.0
        self._robots: Protego | None = None

    async def __aenter__(self) -> BaseCrawler:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._client.aclose()

    async def _respect_rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_at
        if elapsed < self.rate_limit_seconds:
            await asyncio.sleep(self.rate_limit_seconds - elapsed)
        self._last_request_at = time.monotonic()

    async def _load_robots(self, base_url: str) -> None:
        if self._robots is not None:
            return
        robots_url = httpx.URL(base_url).join("/robots.txt")
        try:
            resp = await self._client.get(str(robots_url))
            if resp.status_code == 200:
                self._robots = Protego.parse(resp.text)
            else:
                self._robots = Protego.parse("")
        except httpx.HTTPError as exc:
            log.warning("robots.fetch_failed", source=self.source_id, error=str(exc))
            self._robots = Protego.parse("")

    def _is_allowed(self, url: str) -> bool:
        if self._robots is None:
            return True
        return self._robots.can_fetch(url, self.user_agent)

    async def _get(self, url: str) -> httpx.Response:
        await self._respect_rate_limit()
        await self._load_robots(url)
        if not self._is_allowed(url):
            raise PermissionError(f"robots.txt forbids fetching {url}")
        log.info("crawl.fetch", source=self.source_id, url=url)
        response = await self._client.get(url)
        response.raise_for_status()
        return response

    async def _snapshot(self, url: str) -> RawSnapshot:
        response = await self._get(url)
        body = response.content
        return RawSnapshot(
            source_id=self.source_id,
            url=str(response.url),
            content=body,
            content_type=response.headers.get("content-type", "text/html").split(";")[0],
            content_hash=hashlib.sha256(body).hexdigest(),
        )

    @abstractmethod
    async def fetch_list(self) -> list[RawSnapshot]: ...

    async def fetch_detail(self, snapshot: RawSnapshot) -> RawSnapshot:
        """Default: just re-fetch the URL. Subclasses can override for nested pages."""

        return await self._snapshot(snapshot.url)


class BaseParser(ABC):
    """Common helpers for parsers. Subclasses implement `parse()`.

    Parsers must be deterministic and free of side effects (no I/O).
    """

    source_id: ClassVar[str]
    parser_version: ClassVar[str] = "0.1.0"

    @abstractmethod
    def parse(self, snapshot: RawSnapshot) -> list[ParsedOpportunity]: ...

    @staticmethod
    def coerce_text(value: str | None) -> str | None:
        if not value:
            return None
        return " ".join(value.split())

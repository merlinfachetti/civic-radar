"""Auto-discovery of source plugins by folder convention."""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import yaml

from crawlers.core.models import SourceConfig
from crawlers.core.protocols import SourceCrawler, SourceParser


@dataclass(frozen=True)
class RegisteredSource:
    config: SourceConfig
    crawler_cls: type | None
    parser_cls: type | None


class SourceRegistry:
    """Discovers source plugins in `crawlers/sources/<id>/`.

    Convention:
        crawlers/sources/<id>/config.yaml   — required, parsed via SourceConfig
        crawlers/sources/<id>/crawler.py    — optional, must export `Crawler`
        crawlers/sources/<id>/parser.py     — recommended, must export `Parser`
    """

    SOURCES_ROOT = Path(__file__).resolve().parent.parent / "sources"

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or self.SOURCES_ROOT
        self._cache: dict[str, RegisteredSource] | None = None

    def discover(self) -> dict[str, RegisteredSource]:
        if self._cache is not None:
            return self._cache

        sources: dict[str, RegisteredSource] = {}
        if not self.root.exists():
            self._cache = sources
            return sources

        for source_dir in sorted(self.root.iterdir()):
            if not source_dir.is_dir():
                continue
            config_path = source_dir / "config.yaml"
            if not config_path.exists():
                continue
            try:
                config_data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
                config = SourceConfig.model_validate(config_data)
            except Exception:
                continue

            module_base = f"crawlers.sources.{source_dir.name}"
            crawler_cls = _try_import(module_base + ".crawler", "Crawler")
            parser_cls = _try_import(module_base + ".parser", "Parser")

            sources[config.id] = RegisteredSource(
                config=config, crawler_cls=crawler_cls, parser_cls=parser_cls
            )

        self._cache = sources
        return sources

    def get(self, source_id: str) -> RegisteredSource | None:
        return self.discover().get(source_id)

    def list_ids(self) -> list[str]:
        return list(self.discover().keys())

    def get_parser(self, source_id: str) -> SourceParser | None:
        reg = self.get(source_id)
        if reg is None or reg.parser_cls is None:
            return None
        return cast(SourceParser, reg.parser_cls())

    def get_crawler(self, source_id: str) -> SourceCrawler | None:
        reg = self.get(source_id)
        if reg is None or reg.crawler_cls is None:
            return None
        return cast(SourceCrawler, reg.crawler_cls())


def _try_import(module_path: str, attr: str) -> type | None:
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        return None
    return cast(type | None, getattr(module, attr, None))

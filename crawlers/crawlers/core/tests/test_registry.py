"""Tests for the source registry auto-discovery."""

from __future__ import annotations

from crawlers.core.registry import SourceRegistry


class TestRegistryDiscovery:
    def test_discovers_three_sources(self) -> None:
        registry = SourceRegistry()
        ids = set(registry.list_ids())
        assert {"cebraspe", "fgv", "pci-concursos"}.issubset(ids)

    def test_get_returns_config(self) -> None:
        registry = SourceRegistry()
        cebraspe = registry.get("cebraspe")
        assert cebraspe is not None
        assert cebraspe.config.name == "Cebraspe"
        assert cebraspe.config.parser == "cebraspe_v1"
        assert cebraspe.config.parser_version == "1.0.0"
        assert cebraspe.config.quality_level == "high"

    def test_get_parser_returns_instance(self) -> None:
        registry = SourceRegistry()
        parser = registry.get_parser("fgv")
        assert parser is not None
        assert parser.source_id == "fgv"
        assert parser.parser_version == "1.0.0"

    def test_unknown_id_returns_none(self) -> None:
        registry = SourceRegistry()
        assert registry.get("does-not-exist") is None
        assert registry.get_parser("does-not-exist") is None

"""Unit tests for config / settings."""

from __future__ import annotations

import pytest

from civic_radar.config import Settings


def test_default_settings() -> None:
    settings = Settings()
    assert settings.env in {"development", "test"}
    assert settings.database_url.startswith("sqlite")
    assert settings.is_sqlite


def test_cors_origins_from_csv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "CIVIC_RADAR_CORS_ORIGINS",
        "http://a.com, http://b.com,http://c.com",
    )
    settings = Settings()
    assert settings.cors_origins == [
        "http://a.com",
        "http://b.com",
        "http://c.com",
    ]


def test_cors_origins_from_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CIVIC_RADAR_CORS_ORIGINS", "http://a.com")
    settings = Settings()
    assert settings.cors_origins == ["http://a.com"]


def test_postgres_url_detected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CIVIC_RADAR_DATABASE_URL", "postgresql+asyncpg://u:p@h/db")
    settings = Settings()
    assert not settings.is_sqlite

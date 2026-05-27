"""Application configuration via environment variables."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables.

    All settings are prefixed with `CIVIC_RADAR_` for clarity. For example,
    set `CIVIC_RADAR_DATABASE_URL=...` to override the default DB.
    """

    model_config = SettingsConfigDict(
        env_prefix="CIVIC_RADAR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        populate_by_name=True,
    )

    env: Literal["development", "test", "production"] = "development"

    database_url: str = "sqlite+aiosqlite:///./data/civic_radar.db"

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    log_format: Literal["console", "json"] = "console"

    # Stored as a comma-separated string and exposed as `cors_origins` (list).
    # We avoid `list[str]` here because pydantic-settings tries to JSON-parse
    # complex types from env vars before any validator runs.
    cors_origins_raw: str = Field(default="http://localhost:3000", alias="CIVIC_RADAR_CORS_ORIGINS")

    metrics_enabled: bool = False
    rate_limit_per_minute: int = 60

    raw_snapshot_path: str = "./data/raw_snapshots"
    user_agent: str = "CivicRadar/0.1 (+https://github.com/merlinfachetti/civic-radar)"

    seed_on_startup: bool = False

    @computed_field  # type: ignore[prop-decorator]
    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins_raw.split(",") if origin.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return memoized settings instance."""

    return Settings()

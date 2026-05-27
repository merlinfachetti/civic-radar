"""SQLAlchemy async engine, session factory, and FastAPI dependency."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from civic_radar.config import Settings


class Base(DeclarativeBase):
    """Base declarative class for all ORM models."""


_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def create_engine_and_session(
    settings: Settings,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """Create or return cached engine + session factory."""

    global _engine, _session_factory

    if _engine is None or _session_factory is None:
        kwargs: dict[str, Any] = {
            "echo": False,
            "future": True,
        }
        if settings.is_sqlite:
            kwargs["connect_args"] = {"check_same_thread": False}

        _engine = create_async_engine(settings.database_url, **kwargs)
        _session_factory = async_sessionmaker(_engine, expire_on_commit=False, autoflush=False)

    return _engine, _session_factory


def reset_engine() -> None:
    """Reset cached engine (mainly used in tests)."""

    global _engine, _session_factory
    _engine = None
    _session_factory = None


async def get_session() -> AsyncIterator[AsyncSession]:
    """FastAPI dependency that yields a fresh DB session per request."""

    from civic_radar.config import get_settings

    _, factory = create_engine_and_session(get_settings())
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

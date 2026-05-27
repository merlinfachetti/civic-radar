"""Shared pytest fixtures."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from decimal import Decimal

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

os.environ.setdefault("CIVIC_RADAR_ENV", "test")
os.environ.setdefault("CIVIC_RADAR_DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("CIVIC_RADAR_LOG_LEVEL", "WARNING")

from civic_radar.config import get_settings
from civic_radar.db import session as session_module
from civic_radar.db.models import (
    ConfidenceLevel,
    EducationLevel,
    Opportunity,
    OpportunityStatus,
    Source,
    SourceType,
)
from civic_radar.db.session import Base
from civic_radar.main import _build_app


@pytest_asyncio.fixture(scope="function")
async def engine() -> AsyncIterator[AsyncEngine]:
    """A fresh in-memory SQLite engine per test."""

    eng = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    factory = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    session_module._engine = engine
    session_module._session_factory = factory
    yield factory
    session_module.reset_engine()


@pytest_asyncio.fixture
async def db_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as s:
        yield s


@pytest_asyncio.fixture
async def client(session_factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncClient]:
    get_settings.cache_clear()
    app = _build_app(get_settings())
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_source() -> Source:
    return Source(
        source_id="test-source",
        name="Test Source",
        type=SourceType.BOARD,
        base_url="https://example.com/",
        quality_level=ConfidenceLevel.HIGH,
        parser_name="test_v1",
    )


@pytest.fixture
def sample_opportunity(sample_source: Source) -> Opportunity:
    return Opportunity(
        title="Concurso Teste — Analista de Sistemas",
        organization="Órgão Teste",
        board="cebraspe",
        area="tecnologia",
        position_name="Analista de Sistemas",
        education_level=EducationLevel.SUPERIOR,
        salary_min=Decimal("8000.00"),
        salary_max=Decimal("12000.00"),
        vacancies=10,
        state="SP",
        city="São Paulo",
        status=OpportunityStatus.OPEN,
        source_url="https://example.com/concurso/1",
        confidence_level=ConfidenceLevel.HIGH,
        keywords=["tecnologia", "analista"],
        source=sample_source,
    )


@pytest_asyncio.fixture
async def seeded_db(
    db_session: AsyncSession, sample_source: Source, sample_opportunity: Opportunity
) -> AsyncSession:
    db_session.add(sample_source)
    db_session.add(sample_opportunity)
    await db_session.commit()
    return db_session

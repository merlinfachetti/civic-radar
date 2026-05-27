"""Integration tests for /v1/sources endpoints."""

from __future__ import annotations

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from civic_radar.db.models import ConfidenceLevel, Source, SourceType


class TestListSources:
    async def test_empty(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.get("/v1/sources")
        assert response.status_code == 200
        assert response.json() == {"items": []}

    async def test_with_sources(self, client: AsyncClient, db_session: AsyncSession) -> None:
        db_session.add_all(
            [
                Source(
                    source_id="cebraspe",
                    name="Cebraspe",
                    type=SourceType.BOARD,
                    base_url="https://cebraspe.org.br",
                    quality_level=ConfidenceLevel.HIGH,
                ),
                Source(
                    source_id="fgv",
                    name="FGV",
                    type=SourceType.BOARD,
                    base_url="https://fgv.br",
                    quality_level=ConfidenceLevel.HIGH,
                    enabled=False,
                ),
            ]
        )
        await db_session.commit()

        response = await client.get("/v1/sources")
        assert response.status_code == 200
        body = response.json()
        assert len(body["items"]) == 2
        source_ids = {item["source_id"] for item in body["items"]}
        assert source_ids == {"cebraspe", "fgv"}


class TestGetSource:
    async def test_returns_source(self, client: AsyncClient, db_session: AsyncSession) -> None:
        db_session.add(
            Source(
                source_id="cebraspe",
                name="Cebraspe",
                type=SourceType.BOARD,
                base_url="https://cebraspe.org.br",
                quality_level=ConfidenceLevel.HIGH,
            )
        )
        await db_session.commit()

        response = await client.get("/v1/sources/cebraspe")
        assert response.status_code == 200
        assert response.json()["source_id"] == "cebraspe"

    async def test_404_when_missing(self, client: AsyncClient, db_session: AsyncSession) -> None:
        response = await client.get("/v1/sources/nonexistent")
        assert response.status_code == 404

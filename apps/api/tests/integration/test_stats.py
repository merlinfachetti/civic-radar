"""Integration tests for /v1/stats."""

from __future__ import annotations

from decimal import Decimal

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from civic_radar.db.models import (
    ConfidenceLevel,
    EducationLevel,
    Opportunity,
    OpportunityStatus,
    Source,
    SourceType,
)


class TestStatsEndpoint:
    async def test_empty_db_returns_zeros(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        response = await client.get("/v1/stats")
        assert response.status_code == 200
        body = response.json()
        assert body["total_opportunities"] == 0
        assert body["open_opportunities"] == 0
        assert body["closed_opportunities"] == 0
        assert body["sources"]["total"] == 0

    async def test_populated_db_returns_aggregates(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> None:
        source = Source(
            source_id="cebraspe",
            name="Cebraspe",
            type=SourceType.BOARD,
            base_url="https://cebraspe.org.br",
            quality_level=ConfidenceLevel.HIGH,
        )
        db_session.add(source)

        db_session.add_all(
            [
                Opportunity(
                    title="Open SP TI",
                    organization="X",
                    area="tecnologia",
                    education_level=EducationLevel.SUPERIOR,
                    salary_min=Decimal("5000"),
                    state="SP",
                    status=OpportunityStatus.OPEN,
                    source_url="https://example.com/1",
                    source=source,
                ),
                Opportunity(
                    title="Open RJ Juridico",
                    organization="Y",
                    area="juridica",
                    education_level=EducationLevel.SUPERIOR,
                    salary_min=Decimal("8000"),
                    state="RJ",
                    status=OpportunityStatus.OPEN,
                    source_url="https://example.com/2",
                    source=source,
                ),
                Opportunity(
                    title="Closed MG Admin",
                    organization="Z",
                    area="administrativo",
                    education_level=EducationLevel.MEDIO,
                    state="MG",
                    status=OpportunityStatus.CLOSED,
                    source_url="https://example.com/3",
                    source=source,
                ),
            ]
        )
        await db_session.commit()

        response = await client.get("/v1/stats")
        assert response.status_code == 200
        body = response.json()

        assert body["total_opportunities"] == 3
        assert body["open_opportunities"] == 2
        assert body["closed_opportunities"] == 1
        assert body["by_state"]["SP"] == 1
        assert body["by_state"]["RJ"] == 1
        assert body["by_state"]["MG"] == 1
        assert body["by_area"]["tecnologia"] == 1
        assert body["by_education_level"]["superior"] == 2
        assert body["sources"]["total"] == 1
        assert body["sources"]["healthy"] == 1

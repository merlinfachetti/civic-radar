"""Integration tests for /v1/match."""

from __future__ import annotations

from datetime import date, timedelta
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


class TestMatchEndpoint:
    async def test_returns_sorted_matches(
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

        future = date.today() + timedelta(days=30)
        db_session.add_all(
            [
                Opportunity(
                    title="Match perfeito TI SP",
                    organization="X",
                    area="tecnologia",
                    education_level=EducationLevel.SUPERIOR,
                    salary_min=Decimal("8000"),
                    salary_max=Decimal("12000"),
                    state="SP",
                    status=OpportunityStatus.OPEN,
                    source_url="https://example.com/1",
                    registration_end_date=future,
                    source=source,
                ),
                Opportunity(
                    title="Mismatch jurídico RJ",
                    organization="Y",
                    area="juridica",
                    education_level=EducationLevel.SUPERIOR,
                    salary_min=Decimal("15000"),
                    salary_max=Decimal("18000"),
                    state="RJ",
                    status=OpportunityStatus.OPEN,
                    source_url="https://example.com/2",
                    registration_end_date=future,
                    source=source,
                ),
            ]
        )
        await db_session.commit()

        response = await client.post(
            "/v1/match",
            json={
                "areas": ["tecnologia"],
                "states": ["SP"],
                "education_level": "superior",
                "minimum_salary": 5000,
                "keywords": ["perfeito"],
            },
        )

        assert response.status_code == 200
        body = response.json()
        assert body["total_evaluated"] == 2
        assert body["total_returned"] == 2
        first, second = body["matches"]
        assert first["score"] > second["score"]
        assert first["opportunity"]["area"] == "tecnologia"

    async def test_closed_opportunities_excluded(
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
        db_session.add(
            Opportunity(
                title="Encerrado",
                organization="X",
                area="tecnologia",
                state="SP",
                status=OpportunityStatus.CLOSED,
                source_url="https://example.com/3",
                source=source,
            )
        )
        await db_session.commit()

        response = await client.post("/v1/match", json={})
        assert response.status_code == 200
        body = response.json()
        assert body["total_evaluated"] == 0
        assert body["matches"] == []

    async def test_invalid_profile_returns_422(self, client: AsyncClient) -> None:
        response = await client.post("/v1/match", json={"minimum_salary": -100})
        assert response.status_code == 422

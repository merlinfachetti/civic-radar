"""Integration tests for /v1/opportunities endpoints."""

from __future__ import annotations

from decimal import Decimal

import pytest
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


@pytest.fixture
async def populated_db(db_session: AsyncSession) -> AsyncSession:
    source = Source(
        source_id="cebraspe",
        name="Cebraspe",
        type=SourceType.BOARD,
        base_url="https://cebraspe.org.br",
        quality_level=ConfidenceLevel.HIGH,
    )
    db_session.add(source)

    opps = [
        Opportunity(
            title="Concurso TI SP",
            organization="Tribunal X",
            board="cebraspe",
            area="tecnologia",
            position_name="Analista de Sistemas",
            education_level=EducationLevel.SUPERIOR,
            salary_min=Decimal("8000"),
            salary_max=Decimal("12000"),
            state="SP",
            city="São Paulo",
            status=OpportunityStatus.OPEN,
            source_url="https://cebraspe.org.br/c/1",
            source=source,
        ),
        Opportunity(
            title="Concurso Jurídico RJ",
            organization="Tribunal Y",
            board="cebraspe",
            area="juridica",
            position_name="Procurador",
            education_level=EducationLevel.SUPERIOR,
            salary_min=Decimal("15000"),
            salary_max=Decimal("18000"),
            state="RJ",
            city="Rio de Janeiro",
            status=OpportunityStatus.OPEN,
            source_url="https://cebraspe.org.br/c/2",
            source=source,
        ),
        Opportunity(
            title="Concurso Encerrado",
            organization="Órgão Z",
            board="cebraspe",
            area="administrativo",
            education_level=EducationLevel.MEDIO,
            state="MG",
            status=OpportunityStatus.CLOSED,
            source_url="https://cebraspe.org.br/c/3",
            source=source,
        ),
    ]
    db_session.add_all(opps)
    await db_session.commit()
    return db_session


class TestListOpportunities:
    async def test_default_returns_only_open(
        self, client: AsyncClient, populated_db: AsyncSession
    ) -> None:
        response = await client.get("/v1/opportunities")
        assert response.status_code == 200
        payload = response.json()
        assert payload["pagination"]["total_count"] == 2
        assert all(item["status"] == "open" for item in payload["items"])

    async def test_filter_by_state(self, client: AsyncClient, populated_db: AsyncSession) -> None:
        response = await client.get("/v1/opportunities?state=SP")
        assert response.status_code == 200
        payload = response.json()
        assert payload["pagination"]["total_count"] == 1
        assert payload["items"][0]["state"] == "SP"

    async def test_filter_by_area(self, client: AsyncClient, populated_db: AsyncSession) -> None:
        response = await client.get("/v1/opportunities?area=juridica")
        assert response.status_code == 200
        assert response.json()["pagination"]["total_count"] == 1

    async def test_filter_salary_min(self, client: AsyncClient, populated_db: AsyncSession) -> None:
        response = await client.get("/v1/opportunities?salary_min=14000")
        assert response.status_code == 200
        payload = response.json()
        assert payload["pagination"]["total_count"] == 1
        assert payload["items"][0]["area"] == "juridica"

    async def test_search_query(self, client: AsyncClient, populated_db: AsyncSession) -> None:
        response = await client.get("/v1/opportunities?q=tribunal y")
        assert response.status_code == 200
        assert response.json()["pagination"]["total_count"] == 1

    async def test_invalid_sort_returns_400(
        self, client: AsyncClient, populated_db: AsyncSession
    ) -> None:
        response = await client.get("/v1/opportunities?sort=bogus")
        assert response.status_code == 400

    async def test_status_closed_filter(
        self, client: AsyncClient, populated_db: AsyncSession
    ) -> None:
        response = await client.get("/v1/opportunities?status=closed")
        assert response.status_code == 200
        assert response.json()["pagination"]["total_count"] == 1


class TestGetOpportunity:
    async def test_returns_detail(self, client: AsyncClient, populated_db: AsyncSession) -> None:
        list_resp = await client.get("/v1/opportunities?state=SP")
        first_id = list_resp.json()["items"][0]["id"]
        detail = await client.get(f"/v1/opportunities/{first_id}")
        assert detail.status_code == 200
        body = detail.json()
        assert body["id"] == first_id
        assert "created_at" in body

    async def test_404_when_missing(self, client: AsyncClient, populated_db: AsyncSession) -> None:
        response = await client.get("/v1/opportunities/nonexistent")
        assert response.status_code == 404

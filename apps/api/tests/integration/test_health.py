"""Integration tests for /health and root endpoint."""

from __future__ import annotations

from httpx import AsyncClient


class TestHealthEndpoint:
    async def test_returns_ok_when_db_reachable(self, client: AsyncClient) -> None:
        response = await client.get("/health")
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "ok"
        assert payload["version"]
        assert payload["database"]["status"] == "connected"
        assert isinstance(payload["uptime_seconds"], int)


class TestRootEndpoint:
    async def test_root_returns_metadata(self, client: AsyncClient) -> None:
        response = await client.get("/")
        assert response.status_code == 200
        payload = response.json()
        assert payload["name"] == "civic-radar-api"
        assert payload["docs"] == "/docs"
        assert payload["openapi"] == "/openapi.json"


class TestOpenAPISchema:
    async def test_openapi_spec_is_valid(self, client: AsyncClient) -> None:
        response = await client.get("/openapi.json")
        assert response.status_code == 200
        spec = response.json()
        assert spec["openapi"].startswith("3.")
        assert spec["info"]["title"] == "CivicRadar API"
        paths = spec["paths"]
        assert "/health" in paths
        assert "/v1/opportunities" in paths
        assert "/v1/match" in paths

    async def test_scalar_docs_render(self, client: AsyncClient) -> None:
        response = await client.get("/docs")
        assert response.status_code == 200
        body = response.text.lower()
        assert "scalar" in body or "openapi" in body

"""FastAPI application entrypoint."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from civic_radar import __version__
from civic_radar.api.health import router as health_router
from civic_radar.api.v1 import router as v1_router
from civic_radar.config import Settings, get_settings
from civic_radar.db.session import create_engine_and_session
from civic_radar.logging import configure_logging, get_logger

API_DESCRIPTION = """
## 🛰️ CivicRadar API

Open source radar for Brazilian public career opportunities.

### Highlights

* 📡 **Multi-source ingestion** — crawlers for Cebraspe, FGV, PCI Concursos
* 🎯 **Deterministic match scoring** with explainable reasons
* 🔍 **Rich filtering** (state, area, education, salary, status, board, keywords)
* 📊 **Public statistics** aggregated across all sources
* 🔓 **No authentication required** — public API for civic-tech purposes

### Conventions

* All paths are versioned: `/v1/...`
* Listings return `{ items, pagination }`
* Pagination is **cursor-based** (opaque)
* Errors follow [RFC 7807 Problem Details](https://datatracker.ietf.org/doc/html/rfc7807)

> **Disclaimer:** CivicRadar is not an official source. Always confirm details with
> the original publisher (banca, órgão, diário oficial).
"""

OPENAPI_TAGS = [
    {
        "name": "meta",
        "description": "Service metadata — health, stats, OpenAPI",
    },
    {
        "name": "opportunities",
        "description": "Search, filter and inspect public tenders",
    },
    {
        "name": "sources",
        "description": "Browse monitored data sources",
    },
    {
        "name": "match",
        "description": "Compute deterministic compatibility score for a profile",
    },
]


def _build_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(level=settings.log_level, format_=settings.log_format)
    log = get_logger("civic_radar.startup")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        log.info(
            "civic_radar.starting",
            version=__version__,
            env=settings.env,
            database=settings.database_url.split("@")[-1],
        )
        create_engine_and_session(settings)
        yield
        log.info("civic_radar.shutdown")

    app = FastAPI(
        title="CivicRadar API",
        description=API_DESCRIPTION,
        version=__version__,
        openapi_tags=OPENAPI_TAGS,
        docs_url=None,
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    @app.get("/docs", include_in_schema=False)
    async def scalar_html() -> HTMLResponse:
        return get_scalar_api_reference(
            openapi_url="/openapi.json",
            title="CivicRadar API · Reference",
        )

    @app.get("/", include_in_schema=False)
    async def index() -> dict[str, str]:
        return {
            "name": "civic-radar-api",
            "version": __version__,
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "repository": "https://github.com/merlinfachetti/civic-radar",
        }

    app.include_router(health_router)
    app.include_router(v1_router)

    return app


app = _build_app()

"""Healthcheck endpoint."""

from __future__ import annotations

import time
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from civic_radar import __version__
from civic_radar.db.models import Source
from civic_radar.db.session import get_session

router = APIRouter(tags=["meta"])
_STARTUP_TIME = time.monotonic()


@router.get(
    "/health",
    summary="Healthcheck",
    description=(
        "Returns service status: API version, database connectivity, "
        "and timestamp of the most recent successful source check."
    ),
)
async def health(session: Annotated[AsyncSession, Depends(get_session)]) -> dict[str, Any]:
    db_status = "connected"
    try:
        await session.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = f"error: {type(exc).__name__}"

    last_check = (
        await session.execute(
            select(Source)
            .where(Source.last_successful_check_at.is_not(None))
            .order_by(Source.last_successful_check_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    last_crawl: dict[str, Any] | None = None
    if last_check and last_check.last_successful_check_at:
        last_crawl = {
            "source": last_check.source_id,
            "completed_at": last_check.last_successful_check_at.isoformat(),
        }

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "version": __version__,
        "database": {"status": db_status},
        "last_crawl": last_crawl,
        "uptime_seconds": int(time.monotonic() - _STARTUP_TIME),
    }

"""API v1 routers."""

from fastapi import APIRouter

from civic_radar.api.v1 import match, opportunities, sources, stats

router = APIRouter(prefix="/v1")
router.include_router(opportunities.router)
router.include_router(sources.router)
router.include_router(stats.router)
router.include_router(match.router)

__all__ = ["router"]

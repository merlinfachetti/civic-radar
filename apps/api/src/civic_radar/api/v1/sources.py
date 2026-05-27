"""Sources endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from civic_radar.db.models import Opportunity, Source
from civic_radar.db.session import get_session
from civic_radar.schemas.source import SourceListResponse, SourceRead

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get(
    "",
    response_model=SourceListResponse,
    summary="List monitored sources",
)
async def list_sources(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SourceListResponse:
    stmt = (
        select(
            Source,
            func.count(Opportunity.id).label("items_count"),
        )
        .outerjoin(Opportunity, Opportunity.source_pk == Source.id)
        .group_by(Source.id)
        .order_by(Source.name)
    )
    rows = (await session.execute(stmt)).all()
    items = []
    for source, count in rows:
        item = SourceRead.model_validate(source)
        items.append(item.model_copy(update={"items_count": int(count or 0)}))
    return SourceListResponse(items=items)


@router.get(
    "/{source_id}",
    response_model=SourceRead,
    summary="Source detail",
    responses={404: {"description": "Source not found"}},
)
async def get_source(
    source_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SourceRead:
    stmt = (
        select(
            Source,
            func.count(Opportunity.id).label("items_count"),
        )
        .outerjoin(Opportunity, Opportunity.source_pk == Source.id)
        .where(Source.source_id == source_id)
        .group_by(Source.id)
    )
    row = (await session.execute(stmt)).one_or_none()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    source, count = row
    item = SourceRead.model_validate(source)
    return item.model_copy(update={"items_count": int(count or 0)})

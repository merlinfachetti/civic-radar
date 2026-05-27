"""Opportunities endpoints."""

from __future__ import annotations

import base64
import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from civic_radar.db.models import (
    EducationLevel,
    Opportunity,
    OpportunityStatus,
)
from civic_radar.db.session import get_session
from civic_radar.schemas.opportunity import (
    OpportunityDetailRead,
    OpportunityListResponse,
    OpportunityRead,
    PaginationMeta,
)

router = APIRouter(prefix="/opportunities", tags=["opportunities"])


def _encode_cursor(offset: int) -> str:
    return base64.urlsafe_b64encode(json.dumps({"o": offset}).encode()).decode()


def _decode_cursor(cursor: str | None) -> int:
    if not cursor:
        return 0
    try:
        payload = json.loads(base64.urlsafe_b64decode(cursor.encode()))
        offset = int(payload.get("o", 0))
        return max(0, offset)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cursor"
        ) from exc


@router.get(
    "",
    response_model=OpportunityListResponse,
    summary="List opportunities",
    description=(
        "Paginated list of opportunities with rich filters. "
        "Filters combine with AND. Use `cursor` for next page."
    ),
)
async def list_opportunities(
    session: Annotated[AsyncSession, Depends(get_session)],
    q: Annotated[str | None, Query(description="Full-text search")] = None,
    state: Annotated[list[str] | None, Query(description="2-letter UF codes (repeatable)")] = None,
    city: str | None = None,
    area: Annotated[list[str] | None, Query()] = None,
    education_level: EducationLevel | None = None,
    salary_min: Annotated[float | None, Query(ge=0)] = None,
    status_: Annotated[
        OpportunityStatus | None,
        Query(alias="status", description="Default `open`"),
    ] = None,
    board: str | None = None,
    organization: str | None = None,
    cursor: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    sort: Annotated[
        str,
        Query(
            description=(
                "Sort by field, prefix with `-` for descending. "
                "Allowed: registration_end_date, created_at, salary_max"
            )
        ),
    ] = "-created_at",
) -> OpportunityListResponse:
    stmt = select(Opportunity)

    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(
            or_(
                func.lower(Opportunity.title).like(like),
                func.lower(Opportunity.description).like(like),
                func.lower(Opportunity.position_name).like(like),
                func.lower(Opportunity.organization).like(like),
            )
        )
    if state:
        stmt = stmt.where(Opportunity.state.in_([s.upper() for s in state]))
    if city:
        stmt = stmt.where(func.lower(Opportunity.city) == city.lower())
    if area:
        stmt = stmt.where(Opportunity.area.in_([a.lower() for a in area]))
    if education_level:
        stmt = stmt.where(Opportunity.education_level == education_level)
    if salary_min is not None:
        stmt = stmt.where(
            or_(
                Opportunity.salary_max >= salary_min,
                Opportunity.salary_min >= salary_min,
            )
        )
    effective_status = status_ if status_ is not None else OpportunityStatus.OPEN
    stmt = stmt.where(Opportunity.status == effective_status)
    if board:
        stmt = stmt.where(func.lower(Opportunity.board) == board.lower())
    if organization:
        like_org = f"%{organization.lower()}%"
        stmt = stmt.where(func.lower(Opportunity.organization).like(like_org))

    allowed_sorts = {
        "created_at": Opportunity.created_at,
        "-created_at": Opportunity.created_at.desc(),
        "registration_end_date": Opportunity.registration_end_date,
        "-registration_end_date": Opportunity.registration_end_date.desc(),
        "salary_max": Opportunity.salary_max,
        "-salary_max": Opportunity.salary_max.desc(),
    }
    if sort not in allowed_sorts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort '{sort}'. Allowed: {sorted(allowed_sorts)}",
        )
    stmt = stmt.order_by(allowed_sorts[sort], Opportunity.id)

    count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
    total = (await session.execute(count_stmt)).scalar_one()

    offset = _decode_cursor(cursor)
    rows = (await session.execute(stmt.offset(offset).limit(limit + 1))).scalars().all()

    has_more = len(rows) > limit
    items = rows[:limit]

    return OpportunityListResponse(
        items=[OpportunityRead.model_validate(item) for item in items],
        pagination=PaginationMeta(
            next_cursor=_encode_cursor(offset + limit) if has_more else None,
            has_more=has_more,
            total_count=int(total),
        ),
    )


@router.get(
    "/{opportunity_id}",
    response_model=OpportunityDetailRead,
    summary="Get opportunity detail",
    responses={404: {"description": "Opportunity not found"}},
)
async def get_opportunity(
    opportunity_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OpportunityDetailRead:
    stmt = (
        select(Opportunity)
        .options(selectinload(Opportunity.source))
        .where(Opportunity.id == opportunity_id)
    )
    result = (await session.execute(stmt)).scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opportunity not found")
    return OpportunityDetailRead.model_validate(result)

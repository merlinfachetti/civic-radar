"""Public statistics endpoint."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from civic_radar.db.models import Opportunity, OpportunityStatus, Source
from civic_radar.db.session import get_session
from civic_radar.schemas.stats import (
    SourcesStats,
    StatsLast7Days,
    StatsResponse,
)

router = APIRouter(prefix="/stats", tags=["meta"])


@router.get(
    "",
    response_model=StatsResponse,
    summary="Aggregated public statistics",
)
async def get_stats(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> StatsResponse:
    seven_days_ago = datetime.now(tz=UTC) - timedelta(days=7)

    total = (await session.execute(select(func.count()).select_from(Opportunity))).scalar_one()
    open_count = (
        await session.execute(
            select(func.count())
            .select_from(Opportunity)
            .where(Opportunity.status == OpportunityStatus.OPEN)
        )
    ).scalar_one()
    closed_count = (
        await session.execute(
            select(func.count())
            .select_from(Opportunity)
            .where(Opportunity.status == OpportunityStatus.CLOSED)
        )
    ).scalar_one()

    by_state_rows = (
        await session.execute(
            select(Opportunity.state, func.count())
            .where(Opportunity.state.is_not(None))
            .group_by(Opportunity.state)
            .order_by(func.count().desc())
        )
    ).all()
    by_state = {state: int(count) for state, count in by_state_rows if state}

    by_area_rows = (
        await session.execute(
            select(Opportunity.area, func.count())
            .where(Opportunity.area.is_not(None))
            .group_by(Opportunity.area)
            .order_by(func.count().desc())
        )
    ).all()
    by_area = {area: int(count) for area, count in by_area_rows if area}

    by_edu_rows = (
        await session.execute(
            select(Opportunity.education_level, func.count())
            .where(Opportunity.education_level.is_not(None))
            .group_by(Opportunity.education_level)
        )
    ).all()
    by_edu = {level.value: int(count) for level, count in by_edu_rows if level}

    new_7d = (
        await session.execute(
            select(func.count())
            .select_from(Opportunity)
            .where(Opportunity.created_at >= seven_days_ago)
        )
    ).scalar_one()
    closed_7d = (
        await session.execute(
            select(func.count())
            .select_from(Opportunity)
            .where(
                Opportunity.status == OpportunityStatus.CLOSED,
                Opportunity.updated_at >= seven_days_ago,
            )
        )
    ).scalar_one()

    sources_total = (await session.execute(select(func.count()).select_from(Source))).scalar_one()
    sources_healthy = (
        await session.execute(
            select(func.count()).select_from(Source).where(Source.enabled.is_(True))
        )
    ).scalar_one()

    return StatsResponse(
        total_opportunities=int(total),
        open_opportunities=int(open_count),
        closed_opportunities=int(closed_count),
        by_state=by_state,
        by_area=by_area,
        by_education_level=by_edu,
        last_7_days=StatsLast7Days(
            new_opportunities=int(new_7d),
            closed_opportunities=int(closed_7d),
        ),
        sources=SourcesStats(
            total=int(sources_total),
            healthy=int(sources_healthy),
        ),
    )

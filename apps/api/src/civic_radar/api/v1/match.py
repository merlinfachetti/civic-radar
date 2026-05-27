"""Match endpoint — request-scoped profile scoring."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from civic_radar.db.models import Opportunity, OpportunityStatus
from civic_radar.db.session import get_session
from civic_radar.match import score_opportunity
from civic_radar.schemas.match import (
    MatchProfile,
    MatchResponse,
    MatchResult,
)
from civic_radar.schemas.opportunity import OpportunityRead

router = APIRouter(prefix="/match", tags=["match"])


@router.post(
    "",
    response_model=MatchResponse,
    summary="Compute match scores",
    description=(
        "Returns opportunities ordered by compatibility score with the given profile. "
        "Profile is **not** persisted — every call is fully stateless."
    ),
)
async def compute_match(
    profile: MatchProfile,
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
) -> MatchResponse:
    stmt = select(Opportunity).where(Opportunity.status == OpportunityStatus.OPEN)
    candidates = (await session.execute(stmt)).scalars().all()

    scored = []
    for opp in candidates:
        result = score_opportunity(profile, opp)
        scored.append(
            MatchResult(
                opportunity_id=opp.id,
                opportunity=OpportunityRead.model_validate(opp),
                score=result.score,
                reasons=result.reasons,
            )
        )

    scored.sort(key=lambda r: r.score, reverse=True)
    returned = scored[:limit]

    return MatchResponse(
        matches=returned,
        total_evaluated=len(candidates),
        total_returned=len(returned),
    )

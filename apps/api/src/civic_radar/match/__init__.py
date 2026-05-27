"""Deterministic match scoring engine.

Public API:
    score_opportunity(profile, opp) -> MatchScore
"""

from civic_radar.match.scoring import (
    MAX_SCORE,
    WEIGHTS,
    MatchScore,
    score_opportunity,
)

__all__ = ["MAX_SCORE", "WEIGHTS", "MatchScore", "score_opportunity"]

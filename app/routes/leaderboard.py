"""
GET /leaderboard — Return top sustainability users ranked by EcoPoints.
"""

from fastapi import APIRouter, Query
from typing import List
from app.models.schemas import LeaderboardEntry
from app.services.leaderboard_service import get_leaderboard

router = APIRouter()


@router.get(
    "/",
    response_model=List[LeaderboardEntry],
    summary="Get sustainability leaderboard",
    description="Returns top users ranked by EcoPoints. Default top 10.",
)
async def leaderboard(
    limit: int = Query(10, ge=1, le=50, description="Number of users to return")
):
    results = await get_leaderboard(limit)
    return [
        LeaderboardEntry(
            rank       = entry["rank"],
            name       = entry["name"],
            eco_points = entry["eco_points"],
            badge      = entry["badge"],
        )
        for entry in results
    ]
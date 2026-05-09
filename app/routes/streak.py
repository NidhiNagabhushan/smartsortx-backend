"""
POST /streak — Update daily recycling streak for a user.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import StreakRequest, StreakResponse
from app.services.streak_service import update_streak

router = APIRouter()


@router.post(
    "/",
    response_model=StreakResponse,
    summary="Update daily recycling streak",
    description="Call this once per day after a successful recycling action.",
)
async def streak(req: StreakRequest):

    try:
        result = await update_streak(req.user_id)
        return StreakResponse(
            streak       = result["streak"],
            message      = result["message"],
            bonus_points = result["bonus_points"],
            last_active  = result["last_active"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
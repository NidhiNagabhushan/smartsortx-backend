"""
POST /reward — Add EcoPoints to a user after recycling action.
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import RewardRequest, RewardResponse
from app.services.reward_service import add_points

router = APIRouter()


@router.post(
    "/",
    response_model=RewardResponse,
    summary="Add EcoPoints to a user",
    description="Called after user confirms recycling. Awards points and updates badge.",
)
async def reward(req: RewardRequest):

    # Points must be positive
    if req.points < 0:
        raise HTTPException(
            status_code=400,
            detail="Points must be a positive number."
        )

    result = await add_points(req.user_id, req.points)

    return RewardResponse(
        total_points = result["total_points"],
        badge        = result["badge"],
    )
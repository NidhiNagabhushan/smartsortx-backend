"""
GET /dashboard/{user_id} — Return sustainability statistics for a user.
"""

from fastapi import APIRouter
from app.models.schemas import DashboardResponse
from app.services.dashboard_service import get_dashboard

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=DashboardResponse,
    summary="Get user sustainability dashboard",
    description="Returns eco points, streak, items sorted, carbon saved and weekly progress.",
)
async def dashboard(user_id: str):
    result = await get_dashboard(user_id)
    return DashboardResponse(
        eco_points      = result["eco_points"],
        streak          = result["streak"],
        items_sorted    = result["items_sorted"],
        carbon_saved    = result["carbon_saved"],
        badge           = result["badge"],
        weekly_progress = result["weekly_progress"],
    )
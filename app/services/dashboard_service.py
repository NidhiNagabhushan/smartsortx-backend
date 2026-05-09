"""
Dashboard Service — SmartSort X
Returns sustainability statistics for a user.
"""

from app.database.connection import get_db
from app.utils.helpers import carbon_saved_label, get_badge


async def get_dashboard(user_id: str) -> dict:
    """Get full sustainability dashboard data for a user."""
    db    = get_db()
    users = db["users"]

    user = await users.find_one({"user_id": user_id})

    # If user doesn't exist return empty state
    # (better than throwing an error during demo!)
    if not user:
        return {
            "eco_points":      0,
            "streak":          0,
            "items_sorted":    0,
            "carbon_saved":    "0.0 kg CO₂",
            "badge":           "Eco Beginner 🌱",
            "weekly_progress": [0, 0, 0, 0, 0, 0, 0],
        }

    return {
        "eco_points":      user.get("eco_points", 0),
        "streak":          user.get("streak", 0),
        "items_sorted":    user.get("items_sorted", 0),
        "carbon_saved":    carbon_saved_label(user.get("carbon_saved", 0.0)),
        "badge":           user.get("badge", get_badge(user.get("eco_points", 0))),
        "weekly_progress": user.get("weekly_progress", [0, 0, 0, 0, 0, 0, 0]),
    }
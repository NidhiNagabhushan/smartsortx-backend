"""
Reward Service — SmartSort X
Handles EcoPoints and badge logic.
"""

from datetime import datetime
from app.database.connection import get_db
from app.utils.helpers import get_badge


async def add_points(user_id: str, points: int) -> dict:
    """Add EcoPoints to a user and update their badge."""
    db    = get_db()
    users = db["users"]

    # Check if user exists
    user = await users.find_one({"user_id": user_id})

    if not user:
        # Auto create user if they don't exist yet
        user = {
            "user_id":         user_id,
            "name":            f"User_{user_id[:6]}",
            "eco_points":      0,
            "streak":          0,
            "items_sorted":    0,
            "carbon_saved":    0.0,
            "badge":           "Eco Beginner 🌱",
            "weekly_progress": [0, 0, 0, 0, 0, 0, 0],
            "last_active":     None,
            "created_at":      datetime.utcnow(),
        }
        await users.insert_one(user)

    # Calculate new points and badge
    new_total = user["eco_points"] + points
    new_badge = get_badge(new_total)

    # Update in database
    await users.update_one(
        {"user_id": user_id},
        {"$set": {
            "eco_points": new_total,
            "badge":      new_badge,
        }},
    )

    return {
        "total_points": new_total,
        "badge":        new_badge,
    }
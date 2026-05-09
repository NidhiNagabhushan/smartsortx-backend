"""
Leaderboard Service — SmartSort X
Returns top users ranked by EcoPoints.
"""

from app.database.connection import get_db


async def get_leaderboard(limit: int = 10) -> list:
    """Get top users sorted by EcoPoints."""
    db    = get_db()
    users = db["users"]

    # Sort by eco_points descending, limit results
    cursor = users.find(
        {},
        {"_id": 0, "name": 1, "eco_points": 1, "badge": 1}
    ).sort("eco_points", -1).limit(limit)

    results = []
    rank    = 1

    async for user in cursor:
        results.append({
            "rank":       rank,
            "name":       user.get("name", "Anonymous"),
            "eco_points": user.get("eco_points", 0),
            "badge":      user.get("badge", "Eco Beginner 🌱"),
        })
        rank += 1

    return results
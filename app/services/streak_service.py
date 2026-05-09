"""
Streak Service — SmartSort X
Handles daily recycling streak logic.
"""

from datetime import datetime
from app.database.connection import get_db
from app.utils.helpers import is_same_day, is_yesterday, get_badge

# ── Bonus points for milestone streaks ────────────────────────────────────────
STREAK_BONUSES = {
    3:  5,    # 3  day streak → +5  bonus points
    7:  15,   # 7  day streak → +15 bonus points
    14: 30,   # 14 day streak → +30 bonus points
    30: 75,   # 30 day streak → +75 bonus points
}


async def update_streak(user_id: str) -> dict:
    """Update the daily recycling streak for a user."""
    db    = get_db()
    users = db["users"]
    now   = datetime.utcnow()

    # Find user
    user = await users.find_one({"user_id": user_id})
    if not user:
        raise ValueError(f"User '{user_id}' not found. Call /reward first.")

    last_active     = user.get("last_active")
    current_streak  = user.get("streak", 0)
    bonus           = 0

    # ── Calculate new streak ───────────────────────────────────────────────────
    if last_active is None:
        # First ever recycling action
        new_streak = 1
        message    = "🌱 Great start! Your eco journey begins today!"

    elif is_same_day(last_active, now):
        # Already recycled today — don't double count
        new_streak = current_streak
        message    = f"✅ Already counted today. Streak: {new_streak} days!"

    elif is_yesterday(last_active, now):
        # Consecutive day — extend streak
        new_streak = current_streak + 1
        message    = f"🔥 {new_streak} day streak! Keep it going!"
        bonus      = STREAK_BONUSES.get(new_streak, 0)

    else:
        # Streak broken
        new_streak = 1
        message    = "😔 Streak reset. But every day is a fresh start! 🌱"

    # ── Update weekly progress ─────────────────────────────────────────────────
    weekly  = user.get("weekly_progress", [0, 0, 0, 0, 0, 0, 0])
    day_idx = now.weekday()   # 0=Monday, 6=Sunday
    weekly[day_idx] = weekly[day_idx] + 1

    # ── Calculate new points and badge ─────────────────────────────────────────
    new_points = user.get("eco_points", 0) + bonus
    new_badge  = get_badge(new_points)

    # ── Save to database ───────────────────────────────────────────────────────
    await users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "streak":          new_streak,
                "last_active":     now,
                "eco_points":      new_points,
                "badge":           new_badge,
                "weekly_progress": weekly,
            },
            "$inc": {
                "items_sorted": 1,
            },
        },
    )

    return {
        "streak":       new_streak,
        "message":      message,
        "bonus_points": bonus,
        "last_active":  now.strftime("%Y-%m-%d %H:%M UTC"),
    }
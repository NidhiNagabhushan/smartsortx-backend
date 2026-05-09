"""
Helper utilities — SmartSort X
Shared functions used across services.
"""

from datetime import datetime

# ── Badge tiers (points → badge name) ─────────────────────────────────────────
# The higher the points, the better the badge
BADGE_TIERS = [
    (500, "Planet Guardian 🌍"),
    (300, "Eco Champion 🏆"),
    (150, "Green Hero 🦸"),
    (75,  "Eco Warrior ⚔️"),
    (30,  "Recycler 🔄"),
    (0,   "Eco Beginner 🌱"),
]


def get_badge(points: int) -> str:
    """Return the correct badge based on total points."""
    for threshold, badge in BADGE_TIERS:
        if points >= threshold:
            return badge
    return "Eco Beginner 🌱"


def carbon_saved_label(kg: float) -> str:
    """Format carbon saved nicely for display."""
    return f"{kg:.1f} kg CO₂"


def is_same_day(dt1: datetime, dt2: datetime) -> bool:
    """Check if two datetimes are on the same calendar day."""
    return dt1.date() == dt2.date()


def is_yesterday(dt: datetime, now: datetime) -> bool:
    """Check if dt was yesterday compared to now."""
    from datetime import timedelta
    return (now.date() - dt.date()).days == 1
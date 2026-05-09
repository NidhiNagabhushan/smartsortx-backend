"""
Pydantic Schemas — SmartSort X
These define the shape of all request and response data.
FastAPI uses these for automatic validation and Swagger docs.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ── Prediction ─────────────────────────────────────────────────────────────────
class PredictionResponse(BaseModel):
    item:         str
    category:     str
    bin:          str
    recyclable:   bool
    hazard_level: str
    eco_points:   int
    confidence:   str
    impact:       str
    eco_tip:      str


# ── Reward ─────────────────────────────────────────────────────────────────────
class RewardRequest(BaseModel):
    user_id: str = Field(..., example="user_123")
    points:  int = Field(..., example=10)

class RewardResponse(BaseModel):
    total_points: int
    badge:        str


# ── Dashboard ──────────────────────────────────────────────────────────────────
class DashboardResponse(BaseModel):
    eco_points:      int
    streak:          int
    items_sorted:    int
    carbon_saved:    str
    badge:           str
    weekly_progress: List[int]


# ── Leaderboard ────────────────────────────────────────────────────────────────
class LeaderboardEntry(BaseModel):
    rank:       int
    name:       str
    eco_points: int
    badge:      str


# ── Streak ─────────────────────────────────────────────────────────────────────
class StreakRequest(BaseModel):
    user_id: str = Field(..., example="user_123")

class StreakResponse(BaseModel):
    streak:       int
    message:      str
    bonus_points: int
    last_active:  str
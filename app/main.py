"""
SmartSort X — FastAPI Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.database.connection import connect_db, disconnect_db
from app.routes import predict, reward, streak, dashboard, leaderboard


# ── Lifespan: runs connect_db on startup, disconnect_db on shutdown ────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()


# ── Create the FastAPI app ─────────────────────────────────────────────────────
app = FastAPI(
    title="SmartSort X API",
    description="AI-powered waste segregation + gamification platform 🌱",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,
)

# ── CORS — allows your React frontend to call this API ────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve uploaded images as static files ─────────────────────────────────────
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ── Register All Routes ────────────────────────────────────────────────────────
app.include_router(predict.router,     prefix="/predict",     tags=["AI Prediction"])
app.include_router(reward.router,      prefix="/reward",      tags=["EcoPoints & Badges"])
app.include_router(streak.router,      prefix="/streak",      tags=["Streak"])
app.include_router(dashboard.router,   prefix="/dashboard",   tags=["Dashboard"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["Leaderboard"])


# ── Health check — confirms server is running ─────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
    "status": "🌱 SmartSort X is live!",
    "docs":   "https://smartsortx-backend.onrender.com/docs",
    "version": "1.0.0",
}
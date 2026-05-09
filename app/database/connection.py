"""
MongoDB connection — SmartSort X
Uses Motor (async driver) so it works perfectly with FastAPI's async endpoints.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "smartsortx")

# This will hold our single shared client
client: AsyncIOMotorClient = None


async def connect_db():
    """Called once on app startup — opens the MongoDB connection."""
    global client
    client = AsyncIOMotorClient(MONGO_URI)
    # Ping the DB to confirm connection works
    await client.admin.command("ping")
    print(f"✅ MongoDB connected — database: '{DB_NAME}'")


async def disconnect_db():
    """Called on app shutdown — cleanly closes the connection."""
    global client
    if client:
        client.close()
        print("🔌 MongoDB disconnected")


def get_db():
    """
    Returns the database handle.
    Call this inside any service/route that needs DB access.
    """
    return client[DB_NAME]

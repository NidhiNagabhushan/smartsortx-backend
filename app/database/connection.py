from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "smartsortx")

client: AsyncIOMotorClient = None


async def connect_db():
    global client
    client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
    await client.admin.command("ping")
    print(f"✅ MongoDB connected — database: '{DB_NAME}'")


async def disconnect_db():
    global client
    if client:
        client.close()


def get_db():
    return client[DB_NAME]
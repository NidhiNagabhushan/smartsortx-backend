from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "smartsortx")

client: AsyncIOMotorClient = None


async def connect_db():
    global client
    client = AsyncIOMotorClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,
    )
    await client.admin.command("ping")
    print(f"✅ MongoDB connected — database: '{DB_NAME}'")


async def disconnect_db():
    global client
    if client:
        client.close()
        print("🔌 MongoDB disconnected")


def get_db():
    return client[DB_NAME]
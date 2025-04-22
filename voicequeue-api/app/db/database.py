from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from app.logging.logger import logger

## Client and DB Globals
client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None

async def mongo_connect() -> None:
    global client, db

    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.MONGODB_NAME]
    logger.info(f"{settings.APP_NAME}: Mongo connection established: {db}")

async def mongo_disconnect() -> None:
    global client

    if client is not None:
        client.close()
        logger.info("Mongo connection closed.")

def get_db() -> None | AsyncIOMotorDatabase:
    return db

def get_client() -> None | AsyncIOMotorClient:
    return client
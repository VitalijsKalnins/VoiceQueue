from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


## Client and DB Globals
client: AsyncIOMotorClient = None
db = None

async def mongo_connect():
    global client, db

    client = AsyncIOMotorClient(settings.APP_NAME)
    db = client[settings.MONGODB_NAME]
    print(f"{settings.APP_NAME}: Mongo connection established: {db} {settings.model_dump()}")


async def mongo_disconnect():
    global client

    if client is not None:
        client.close()
        print("Mongo connection closed")
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.db.database import get_db, get_client
from app.logging.logger import logger


class ProfilesRepository():
    ## Profiles collection index
    COLLECTION = "profiles"

    def __init__(self):
        self._db: AsyncIOMotorDatabase = None
        self._client: AsyncIOMotorClient = None

    @property
    def db(self) -> None | AsyncIOMotorDatabase:
        if self._db is None:
            self._db = get_db()
        return self._db
    
    @property
    def client(self) -> None | AsyncIOMotorClient:
        if self._client is None:
            self._client = get_client()
        return self._client
    
    async def test_save(self, param):
        result = await self.db[self.COLLECTION].insert_one(param)
        return result

## Profiles Repository Singleton
repository = ProfilesRepository()
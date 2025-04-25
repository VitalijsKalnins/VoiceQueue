from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.db.database import get_db, get_client
from app.logging.logger import logger
from app.entity.profile import Profile

from typing import List, Dict

class ProfilesRepository():
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
    
    async def get_profile(self, profile_id: int) -> Profile | None:
        res: Profile | None = None

        ## Query for profile_id
        serialized = await self.db[self.COLLECTION].find_one({"_id": profile_id})

        ## if a profile with profile_id is found, we must
        ## create a new profile obj. from the serialized data
        if not serialized is None:
            res = Profile.from_dict(serialized)

        return res

    async def get_profiles(self, profile_ids: List[int]) -> Dict:
        ## Resulting dictionary of profile_id -> profile obj.
        res: Dict = {}

        ## Query for all ids in List -> assign to resulting dict
        cursor = self.db[self.COLLECTION].find({"_id": {"$in": profile_ids}})
        for serialized in await cursor.to_list(length=64):
            profile = Profile.from_dict(serialized)
            res[profile.id] = profile

        return res
    
    async def set_profile(self, profile: Profile) -> bool:
        res = await self.db[self.COLLECTION].replace_one({"_id": profile.id}, profile.to_dict(), upsert=True)
        return (res.modified_count == 1 or res.did_upsert)

## Profiles Repository Singleton
repository = ProfilesRepository()
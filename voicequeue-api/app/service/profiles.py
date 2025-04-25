from app.entity.profile import Profile
from app.entity.profile_entity import ProfileEntity
from app.enum.profiles import ProfileEntityType
from app.service.nlp import service as NLPService
from app.repository.profiles import repository as ProfilesRepository
from app.logging.logger import logger

from typing import List, Dict

class Profiles:
    async def get_profile(self, profile_id: int) -> Profile:
        ## to-do: add a default profile for users that have not yet set their profile
        return await ProfilesRepository.get_profile(profile_id)

    async def get_profiles(self, profile_ids: List[int]) -> Dict:
        return await ProfilesRepository.get_profiles(profile_ids)
    
    ## to-do: change this method to accept id, raw input str
    async def set_profile(self, profile: Profile) -> bool:
        return await ProfilesRepository.set_profile(profile)

## Profile Service Singleton
service = Profiles()
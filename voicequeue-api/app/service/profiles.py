from app.entity.profile import Profile
from app.entity.profile_entity import ProfileEntity
from app.enum.profiles import ProfileEntityType
from app.service.nlp import service as NLPService
from app.repository.profiles import repository as ProfilesRepository
from app.logging.logger import logger

class Profiles:
    async def GetProfile(profile_id: int) -> Profile:
        profile_ent1 = ProfileEntity("football", ProfileEntityType.INTEREST, 0.8, [1, 2, 3])
        new_profile = Profile(123, "I love football.", [profile_ent1])
        serialized = new_profile.to_dict()

        ##res = await ProfilesRepository.test_save(serialized)
        ##logger.info(f"result: {res}")

## Profile Service Singleton
service = Profiles()
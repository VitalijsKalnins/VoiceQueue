from app.entity.profile import Profile

class Profiles:
    def GetProfile(profile_id: int) -> Profile:
        pass

## Profile Service Singleton
service = Profiles()
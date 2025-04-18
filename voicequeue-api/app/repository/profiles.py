from app.db.database import get_db


class ProfilesRepository():
    COLLECTION = "profiles"

    def __init__(self):
        self._db = None

    @property
    def db(self):
        if self._db is None:
            self._db = get_db()
        return self._db

## Profiles Repository Singleton
profiles_repository = ProfilesRepository()
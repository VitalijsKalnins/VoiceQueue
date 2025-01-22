from pydantic import BaseSettings

class Settings(BaseSettings):
    ## Defaults for local dev
    APP_NAME: str = "VoiceQueue API"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_NAME: str = "voicequeue_db"

    class Config:
        env_file = ".env"

settings = Settings()
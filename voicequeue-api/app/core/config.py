from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ## Defaults for local dev
    APP_NAME: str = "VoiceQueue API (Local Env)"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_NAME: str = "voicequeue_db"

    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()
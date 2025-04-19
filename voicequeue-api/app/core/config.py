from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ## Defaults for local dev env
    ## Deploy with: "uvicorn app.main:app --env-file app/prod.env" for prod env
    ## Deploy with: "uvicorn app.main:app --env-file app/staging.env" for staging env
    APP_NAME: str = "VoiceQueue API (Local Env)"
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_NAME: str = "voicequeue_db"
    
    ## Provided in staging and prod .env files
    OPENAI_API_KEY: str = "sk-..."
    OPENAI_API_ORG: str = "org-..."

    ## Settings config
    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()
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

    ## Pre-trained spaCy model selection
    SPACY_MODEL: str = "en"
    SPACY_LLM_FAMILY: str = "spacy.GPT-4.v3"
    SPACY_LLM_MODEL: str = "gpt-4o-mini"

    ## NLP embedding model selection
    ## https://sbert.net/docs/sentence_transformer/pretrained_models.html
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    ## Disable HuggingFace symlink warning
    HF_HUB_DISABLE_SYMLINKS_WARNING: bool = True

    ## Settings config
    model_config = SettingsConfigDict(extra="ignore")

settings = Settings()
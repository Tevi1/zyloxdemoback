# Settings (.env → pydantic-settings)
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_ORG_ID: str | None = None
    OPENAI_PROJECT_ID: str | None = None

    VECTOR_STORE_LEGAL: str
    VECTOR_STORE_MARKETING: str
    VECTOR_STORE_OPS: str
    VECTOR_STORE_STRATEGY: str
    VECTOR_STORE_ANALYST: str
    VECTOR_STORE_FINANCE: str

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_ENV: str = "dev"
    CORS_ALLOW_ORIGINS: str = "*"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()


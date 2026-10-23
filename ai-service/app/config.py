from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Deployment config. Values come from the environment or .env (gitignored)."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str  # vector DB, owned by this service; no default (holds credentials)
    ollama_url: str = "http://localhost:11434"
    redis_url: str = "redis://localhost:6379"
    s3_endpoint: str = "http://localhost:9000"


@lru_cache
def get_settings() -> Settings:
    return Settings()

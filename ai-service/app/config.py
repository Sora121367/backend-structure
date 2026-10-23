from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_SERVICE_DIR = Path(__file__).resolve().parent.parent

# Repo-root .env (copied from .env.example) first; an optional ai-service/.env overrides it.
ENV_FILES = (_SERVICE_DIR.parent / ".env", _SERVICE_DIR / ".env")


class Settings(BaseSettings):
    """Deployment config. Values come from the environment or .env (gitignored)."""

    model_config = SettingsConfigDict(env_file=ENV_FILES, extra="ignore")

    database_url: str  # vector DB, owned by this service; no default (holds credentials)
    ollama_url: str = "http://localhost:11434"
    redis_url: str = "redis://localhost:6379"
    s3_endpoint: str = "http://localhost:9000"

    # Service-token auth: Spring Boot calls with a client-credentials token from Keycloak.
    keycloak_issuer: str  # must equal the token's `iss`
    keycloak_jwks_url: str | None = None  # where to fetch signing keys; set it inside containers
    keycloak_audience: str | None = None  # checked only when set (needs a realm audience mapper)
    service_client_id: str = "insighthub-ai-caller"  # the token's `azp`

    @property
    def jwks_url(self) -> str:
        if self.keycloak_jwks_url:
            return self.keycloak_jwks_url
        return f"{self.keycloak_issuer.rstrip('/')}/protocol/openid-connect/certs"


@lru_cache
def get_settings() -> Settings:
    return Settings()

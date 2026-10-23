import pytest
from pydantic import ValidationError

from app.config import Settings

ISSUER = "http://localhost:8180/realms/insighthub"


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    for name in ("DATABASE_URL", "REDIS_URL", "KEYCLOAK_ISSUER", "KEYCLOAK_JWKS_URL"):
        monkeypatch.delenv(name, raising=False)


def write_env(tmp_path, text):
    env_file = tmp_path / ".env"
    env_file.write_text(text)
    return env_file


def test_reads_values_from_env_file(tmp_path):
    env_file = write_env(
        tmp_path,
        "DATABASE_URL=postgresql://ai:ai@localhost:5433/vectors   # vector DB\n"
        "REDIS_URL=redis://example:6379\n"
        f"KEYCLOAK_ISSUER={ISSUER}\n",
    )

    settings = Settings(_env_file=env_file)

    assert settings.database_url == "postgresql://ai:ai@localhost:5433/vectors"
    assert settings.redis_url == "redis://example:6379"
    assert settings.keycloak_issuer == ISSUER
    assert settings.service_client_id == "insighthub-ai-caller"


def test_environment_overrides_env_file(tmp_path, monkeypatch):
    env_file = write_env(
        tmp_path, f"DATABASE_URL=postgresql://from-file/db\nKEYCLOAK_ISSUER={ISSUER}\n"
    )
    monkeypatch.setenv("DATABASE_URL", "postgresql://from-env/db")

    assert Settings(_env_file=env_file).database_url == "postgresql://from-env/db"


@pytest.mark.parametrize("missing", ["DATABASE_URL", "KEYCLOAK_ISSUER"])
def test_required_settings(tmp_path, missing):
    values = {"DATABASE_URL": "postgresql://x/db", "KEYCLOAK_ISSUER": ISSUER}
    del values[missing]
    env_file = write_env(tmp_path, "".join(f"{k}={v}\n" for k, v in values.items()))

    with pytest.raises(ValidationError):
        Settings(_env_file=env_file)


def test_jwks_url_defaults_to_issuer_certs_endpoint():
    settings = Settings(_env_file=None, database_url="postgresql://x/db", keycloak_issuer=ISSUER)

    assert settings.jwks_url == f"{ISSUER}/protocol/openid-connect/certs"


def test_jwks_url_can_be_overridden_for_containers():
    url = "http://keycloak:8080/realms/insighthub/protocol/openid-connect/certs"
    settings = Settings(
        _env_file=None,
        database_url="postgresql://x/db",
        keycloak_issuer=ISSUER,
        keycloak_jwks_url=url,
    )

    assert settings.jwks_url == url

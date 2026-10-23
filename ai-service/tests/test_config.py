import pytest
from pydantic import ValidationError

from app.config import Settings


def test_reads_values_from_env_file(tmp_path, monkeypatch):
    for name in ("DATABASE_URL", "REDIS_URL"):
        monkeypatch.delenv(name, raising=False)
    env_file = tmp_path / ".env"
    env_file.write_text(
        "DATABASE_URL=postgresql://ai:ai@localhost:5433/vectors   # vector DB\n"
        "REDIS_URL=redis://example:6379\n"
    )

    settings = Settings(_env_file=env_file)

    assert settings.database_url == "postgresql://ai:ai@localhost:5433/vectors"
    assert settings.redis_url == "redis://example:6379"


def test_environment_overrides_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("DATABASE_URL=postgresql://from-file/db\n")
    monkeypatch.setenv("DATABASE_URL", "postgresql://from-env/db")

    assert Settings(_env_file=env_file).database_url == "postgresql://from-env/db"


def test_database_url_is_required(tmp_path, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=tmp_path / "missing.env")

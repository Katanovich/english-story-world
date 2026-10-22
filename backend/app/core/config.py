from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# .env lives at the repository root (one level above backend/)
_ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_ROOT_ENV, extra="ignore")

    app_env: str = "development"
    api_prefix: str = "/api/v1"

    database_url: str
    test_database_url: str | None = None

    secret_key: str
    session_ttl_hours: int = 72
    session_cookie_name: str = "esw_session"
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:3000"]

    admin_email: str | None = None
    admin_username: str | None = None
    admin_password: str | None = None

    storage_backend: str = "local"
    local_storage_dir: str = "./media_storage"
    max_image_mb: int = 5
    max_audio_mb: int = 20
    max_video_mb: int = 500

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str) and not value.startswith("["):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()

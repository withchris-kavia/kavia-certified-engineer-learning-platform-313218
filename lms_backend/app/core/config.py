"""Application configuration loaded from environment variables.

This module defines the Settings object used across the service.
"""

from __future__ import annotations

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings loaded from environment (.env)."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="Kavia LMS Backend", description="Human readable application name.")
    app_version: str = Field(default="0.1.0", description="Application semantic version.")
    app_env: str = Field(default="development", description="Environment name (development/staging/production).")

    host: str = Field(default="0.0.0.0", description="Host interface to bind the server to.")
    port: int = Field(default=3001, description="Port to bind the server to (preview system uses 3001).")

    database_url: str = Field(
        ...,
        alias="DATABASE_URL",
        description="Async SQLAlchemy database URL, e.g. postgresql+asyncpg://user:pass@host:port/db",
    )

    jwt_secret_key: str = Field(
        ...,
        alias="JWT_SECRET_KEY",
        description="Secret key used to sign JWT tokens. MUST be set via environment.",
    )
    jwt_algorithm: str = Field(
        default="HS256",
        alias="JWT_ALGORITHM",
        description="JWT signing algorithm.",
    )
    access_token_expire_minutes: int = Field(
        default=60,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="JWT access token expiration in minutes.",
    )

    cors_origins: str = Field(
        default="http://127.0.0.1:3000",
        alias="CORS_ORIGINS",
        description="Comma-separated list of allowed CORS origins.",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list of strings."""
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()

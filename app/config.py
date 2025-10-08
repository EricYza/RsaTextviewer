"""Application configuration settings."""

from __future__ import annotations

import os
from typing import Dict, Optional, Type
from urllib.parse import quote_plus


def _build_postgres_uri() -> Optional[str]:
    """Construct a SQLAlchemy URI for Azure PostgreSQL when env vars are present."""

    user = os.environ.get("POSTGRES_USER", "bsgwfnomek")
    password = os.environ.get("POSTGRES_PASSWORD")
    host = os.environ.get("POSTGRES_HOST", "text-server.postgres.database.azure.com")
    port = os.environ.get("POSTGRES_PORT", "5432")
    database = os.environ.get("POSTGRES_DB", "postgres")

    if not password:
        return None

    safe_password = quote_plus(password)
    return (
        f"postgresql+psycopg2://{user}:{safe_password}@{host}:{port}/{database}"
        "?sslmode=require"
    )


class Config:
    """Base configuration with sane defaults for local development."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = (
        _build_postgres_uri()
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit
    UPLOAD_ALLOWED_EXTENSIONS = frozenset({"txt"})


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        _build_postgres_uri()
    )


class ProductionConfig(Config):
    DEBUG = False


CONFIG_MAP: Dict[str, Type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(name: str | None) -> Type[Config]:
    """Return the configuration class for a given name."""
    if not name:
        return Config
    return CONFIG_MAP.get(name.lower(), Config)

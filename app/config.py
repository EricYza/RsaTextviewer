"""Application configuration settings."""

from __future__ import annotations

import os
from typing import Dict, Type


class Config:
    """Base configuration with sane defaults for local development."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///textviewer.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit
    UPLOAD_ALLOWED_EXTENSIONS = frozenset({"txt"})


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL", "sqlite:///:memory:"
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

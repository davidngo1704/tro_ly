"""Application configuration module.

This module contains all configuration settings for the FastAPI application,
including database and authentication settings.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables.
    
    Attributes:
        database_url (str): Database connection URL.
        secret_key (str): Secret key for authentication (default: 'dev').
    """
    database_url: str
    secret_key: str = "dev"

    class Config:
        """Pydantic configuration for loading settings from .env file."""
        env_file = ".env"

settings = Settings()
"""Global application settings instance."""

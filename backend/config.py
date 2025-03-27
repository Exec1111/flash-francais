from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Environnement (development, production)
    ENV: str = "development"
    
    # Configuration de la base de données
    DATABASE_URL: str
    
    # Configuration de l'API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Flash Français API"
    
    # Configuration de sécurité
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]  # Frontend URL
    
    # Swagger UI (désactivé en production)
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"
    OPENAPI_URL: str | None = "/openapi.json"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List
import os

class Settings(BaseSettings):
    # Environnement (development, production)
    ENV: str = "development"
    
    # Configuration de la base de données
    DATABASE_URL: str = ""
    
    # Configuration de l'API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Flash Français API"
    
    # Configuration de sécurité
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"  # Frontend URL
    
    # Swagger UI (peut être désactivé en production via .env.production)
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"
    OPENAPI_URL: str | None = "/openapi.json"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    
    # Vérifier si nous sommes sur Render
    if os.environ.get("RENDER") == "true":
        # Forcer le mode production
        settings.ENV = "production"
        
        # Récupérer l'URL de la base de données directement depuis les variables d'environnement
        render_db_url = os.environ.get("DATABASE_URL")
        if render_db_url:
            settings.DATABASE_URL = render_db_url
        
        # Les paramètres de documentation sont déjà définis par .env.production
        # Nous ne les modifions pas ici pour éviter les conflits
    
    return settings

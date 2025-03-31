from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db, engine, Base
from config import get_settings, Settings
from routers import auth_router

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    API pour l'application Flash Français. Permet de gérer les utilisateurs et l'authentification.
    
    ## Authentification
    
    * Inscription d'un nouvel utilisateur
    * Connexion pour obtenir un token JWT
    * Récupération des informations de l'utilisateur connecté
    """,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Opérations d'authentification"
        }
    ],
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL
)

# Configuration CORS
origins = [
    "http://localhost:3000",  # Frontend React
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes d'authentification
app.include_router(
    auth_router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["auth"]
)

@app.get("/", tags=["root"])
def root():
    return {"message": "Bienvenue sur l'API Flash Français"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

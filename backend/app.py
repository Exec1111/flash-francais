from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import crud.flashcard as crud
from schemas.flashcard import Flashcard, FlashcardCreate
from config import get_settings, Settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    API pour l'application Flash Français. Permet de gérer les flashcards pour l'apprentissage du français.
    
    ## Flashcards
    
    Vous pouvez :
    * Créer des flashcards
    * Lire les flashcards
    * Mettre à jour les flashcards
    * Supprimer les flashcards
    """,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "flashcards",
            "description": "Opérations sur les flashcards"
        }
    ],
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Bienvenue sur l'API Flash Français!"}

@app.post("/flashcards/", response_model=Flashcard, tags=["flashcards"])
def create_flashcard(flashcard: FlashcardCreate, db: Session = Depends(get_db)):
    """
    Créer une nouvelle flashcard avec :
    - **french_word**: le mot en français
    - **english_translation**: la traduction en anglais
    - **example_sentence**: une phrase d'exemple (optionnel)
    """
    return crud.create_flashcard(db=db, flashcard=flashcard)

@app.get("/flashcards/", response_model=List[Flashcard], tags=["flashcards"])
def read_flashcards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupérer la liste des flashcards avec pagination.
    """
    flashcards = crud.get_flashcards(db, skip=skip, limit=limit)
    return flashcards

@app.get("/flashcards/{flashcard_id}", response_model=Flashcard, tags=["flashcards"])
def read_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    """
    Récupérer une flashcard spécifique par son ID.
    """
    db_flashcard = crud.get_flashcard(db, flashcard_id=flashcard_id)
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard non trouvée")
    return db_flashcard

@app.put("/flashcards/{flashcard_id}", response_model=Flashcard, tags=["flashcards"])
def update_flashcard(flashcard_id: int, flashcard: FlashcardCreate, db: Session = Depends(get_db)):
    """
    Mettre à jour une flashcard existante.
    """
    db_flashcard = crud.update_flashcard(db, flashcard_id=flashcard_id, flashcard=flashcard)
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard non trouvée")
    return db_flashcard

@app.delete("/flashcards/{flashcard_id}", response_model=Flashcard, tags=["flashcards"])
def delete_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    """
    Supprimer une flashcard.
    """
    db_flashcard = crud.delete_flashcard(db, flashcard_id=flashcard_id)
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard non trouvée")
    return db_flashcard

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)

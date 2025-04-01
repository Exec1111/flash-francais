from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import crud
from schemas.progression import ProgressionCreate, ProgressionRead, ProgressionUpdate

router = APIRouter(
    # prefix="/progressions", # Supprimé car géré dans app.py
    tags=["progressions"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ProgressionRead, name="create_progression")
def create_progression_endpoint(progression: ProgressionCreate, db: Session = Depends(get_db)):
    return crud.create_progression(db=db, progression=progression)

@router.get("/", response_model=List[ProgressionRead])
def read_progressions_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    progressions = crud.get_progressions(db, skip=skip, limit=limit)
    return progressions

@router.get("/{progression_id}", response_model=ProgressionRead)
def read_progression_route(progression_id: int, db: Session = Depends(get_db)):
    db_progression = crud.get_progression(db, progression_id=progression_id)
    if db_progression is None:
        raise HTTPException(status_code=404, detail="Progression not found")
    return db_progression

@router.put("/{progression_id}", response_model=ProgressionRead)
def update_progression_route(progression_id: int, progression: ProgressionUpdate, db: Session = Depends(get_db)):
    db_progression = crud.update_progression(db=db, progression_id=progression_id, progression_update=progression)
    if db_progression is None:
        raise HTTPException(status_code=404, detail="Progression not found")
    return db_progression

@router.delete("/{progression_id}", status_code=204) # No content on successful deletion
def delete_progression_route(progression_id: int, db: Session = Depends(get_db)):
    success = crud.delete_progression(db, progression_id=progression_id)
    if not success:
        raise HTTPException(status_code=404, detail="Progression not found")
    return # Return None for 204 status code

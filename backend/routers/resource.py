from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import crud
from schemas.resource import ResourceCreate, ResourceRead, ResourceUpdate
from models.user import User
from security import get_current_active_user
import logging
logger = logging.getLogger(__name__)

resource_router = APIRouter(
    # prefix="/resources", # Supprimé car géré dans app.py
    tags=["resources"],
    responses={404: {"description": "Not found"}},
)

@resource_router.post("/", response_model=ResourceRead)
def create_resource_route(resource: ResourceCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_resource(db=db, resource=resource)
    except ValueError as e:
        # Intercepter l'erreur si session_id est invalide
        raise HTTPException(status_code=404, detail=str(e))

@resource_router.get("/", response_model=List[ResourceRead])
def read_resources_route(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Récupère les ressources appartenant à l'utilisateur connecté."""
    logger.info(f"Récupération des ressources pour l'utilisateur {current_user.id}")
    resources = crud.get_resources(db, user_id=current_user.id, skip=skip, limit=limit)
    logger.info(f"Nombre de ressources trouvées : {len(resources)}")
    return resources

@resource_router.get("/standalone", response_model=List[ResourceRead])
def read_resources_standalone_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    resources = crud.get_resources_standalone(db, skip=skip, limit=limit)
    return resources

@resource_router.get("/by_session/{session_id}", response_model=List[ResourceRead])
def read_resources_by_session_route(session_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Vérifier si la session parente existe
    db_session = crud.get_session(db, session_id=session_id)
    if db_session is None:
        raise HTTPException(status_code=404, detail=f"Session with id {session_id} not found")
    resources = crud.get_resources_by_session(db, session_id=session_id, skip=skip, limit=limit)
    return resources

@resource_router.get("/{resource_id}", response_model=ResourceRead)
def read_resource_route(resource_id: int, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id=resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@resource_router.put("/{resource_id}", response_model=ResourceRead)
def update_resource_route(resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)):
    try:
        db_resource = crud.update_resource(db=db, resource_id=resource_id, resource_update=resource)
        if db_resource is None:
            raise HTTPException(status_code=404, detail="Resource not found")
        return db_resource
    except ValueError as e:
        # Intercepter l'erreur si le nouveau session_id est invalide
        raise HTTPException(status_code=404, detail=str(e))

@resource_router.delete("/{resource_id}", status_code=204)
def delete_resource_route(resource_id: int, db: Session = Depends(get_db)):
    success = crud.delete_resource(db, resource_id=resource_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resource not found")
    return # Retourne None pour 204

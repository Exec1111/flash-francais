from pydantic import BaseModel, Json
from typing import Any, Optional, List
from models.resource import ResourceType # Importer l'Enum depuis les modèles

class ResourceBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: ResourceType
    content: Optional[Any] = None # Accepte n'importe quelle structure JSON valide ou None
    session_ids: Optional[List[int]] = [] # Liste des IDs des sessions associées
    user_id: int  # ID de l'utilisateur propriétaire de la ressource

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel): # Permettre les mises à jour partielles
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ResourceType] = None
    content: Optional[Any] = None
    session_ids: Optional[List[int]] = None # Peut être mis à jour (ajouter/retirer des sessions)
    user_id: Optional[int] = None # Peut être mis à jour (changer de propriétaire)

class ResourceRead(ResourceBase):
    id: int
    session_ids: List[int]  # Liste des IDs des sessions associées

    class Config:
        from_attributes = True # Compatible avec l'ORM SQLAlchemy

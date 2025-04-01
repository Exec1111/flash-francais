from pydantic import BaseModel, Json
from typing import Any, Optional
from models.resource import ResourceType # Importer l'Enum depuis les modèles

class ResourceBase(BaseModel):
    title: str
    description: Optional[str] = None
    type: ResourceType
    content: Optional[Any] = None # Accepte n'importe quelle structure JSON valide ou None
    session_id: Optional[int] = None # session_id est optionnel

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel): # Permettre les mises à jour partielles
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ResourceType] = None
    content: Optional[Any] = None
    session_id: Optional[int] = None # Peut être mis à jour (ajouter/retirer d'une session)

class ResourceRead(ResourceBase):
    id: int

    class Config:
        from_attributes = True # Compatible avec l'ORM SQLAlchemy

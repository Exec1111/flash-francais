from sqlalchemy.orm import Session
from models import Resource, Session # Import Resource model and Session for checking session_id
from schemas.resource import ResourceCreate, ResourceUpdate # Import schemas
from sqlalchemy import or_

def get_resource(db: Session, resource_id: int):
    """Récupère une ressource par son ID."""
    return db.query(Resource).filter(Resource.id == resource_id).first()

def get_resources(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de toutes les ressources (liées ou non à une session)."""
    return db.query(Resource).offset(skip).limit(limit).all()

def get_resources_by_session(db: Session, session_id: int, skip: int = 0, limit: int = 100):
    """Récupère les ressources appartenant à une session spécifique."""
    return db.query(Resource).filter(Resource.session_id == session_id).offset(skip).limit(limit).all()

def get_resources_standalone(db: Session, skip: int = 0, limit: int = 100):
    """Récupère les ressources qui ne sont liées à aucune session."""
    return db.query(Resource).filter(Resource.session_id == None).offset(skip).limit(limit).all()

def create_resource(db: Session, resource: ResourceCreate):
    """Crée une nouvelle ressource."""
    # Vérifier si session_id est fourni et s'il correspond à une session existante
    if resource.session_id is not None:
        db_session = db.query(Session).filter(Session.id == resource.session_id).first()
        if not db_session:
            # Gérer l'erreur : Session non trouvée
            # On pourrait lever une exception ou retourner None/False
            raise ValueError(f"Session with id {resource.session_id} not found") # Exemple d'exception

    db_resource = Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def update_resource(db: Session, resource_id: int, resource_update: ResourceUpdate):
    """Met à jour une ressource existante."""
    db_resource = get_resource(db, resource_id=resource_id)
    if db_resource is None:
        return None

    update_data = resource_update.model_dump(exclude_unset=True)

    # Vérifier si le nouveau session_id (s'il est fourni) existe
    if 'session_id' in update_data and update_data['session_id'] is not None:
        db_session = db.query(Session).filter(Session.id == update_data['session_id']).first()
        if not db_session:
            raise ValueError(f"Session with id {update_data['session_id']} not found")

    for key, value in update_data.items():
        setattr(db_resource, key, value)

    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def delete_resource(db: Session, resource_id: int):
    """Supprime une ressource par son ID."""
    db_resource = get_resource(db, resource_id=resource_id)
    if db_resource is None:
        return None # Ou False
    db.delete(db_resource)
    db.commit()
    return True # Confirme la suppression

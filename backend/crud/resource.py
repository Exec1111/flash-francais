from sqlalchemy.orm import Session
from models import Resource, Session, User # Import Resource model, Session for checking session_id and User for checking user_id
from schemas.resource import ResourceCreate, ResourceUpdate # Import schemas
from sqlalchemy import or_
import logging
logger = logging.getLogger(__name__)

def get_resource(db: Session, resource_id: int):
    """Récupère une ressource par son ID."""
    return db.query(Resource).filter(Resource.id == resource_id).first()

def get_resources(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Récupère une liste des ressources appartenant à un utilisateur spécifique."""
    logger.info(f"Recherche des ressources pour l'utilisateur {user_id}")
    # Récupérer les ressources avec les sessions associées, filtrées par user_id
    resources = db.query(Resource).filter(Resource.user_id == user_id).offset(skip).limit(limit).all()
    logger.info(f"Nombre de ressources trouvées pour l'utilisateur {user_id}: {len(resources)}")
    
    # Créer la liste des ressources avec leurs IDs de sessions
    resources_with_sessions = []
    for resource in resources:
        logger.info(f"Récupération des sessions pour la ressource {resource.id}")
        resource_data = {
            "id": resource.id,
            "title": resource.title,
            "description": resource.description,
            "type": resource.type,
            "content": resource.content,
            "user_id": resource.user_id,
            "session_ids": [session.id for session in resource.sessions]
        }
        resources_with_sessions.append(resource_data)
    
    return resources_with_sessions

def get_resources_by_session(db: Session, session_id: int, skip: int = 0, limit: int = 100):
    """Récupère les ressources appartenant à une session spécifique."""
    from models.resource import Resource
    from models.association_tables import session_resource_association
    
    try:
        logger.info(f"Recherche des ressources pour la session {session_id}")
        
        # Utiliser une jointure avec la table d'association
        resources = db.query(Resource).\
            join(session_resource_association, session_resource_association.c.resource_id == Resource.id).\
            filter(session_resource_association.c.session_id == session_id).\
            offset(skip).limit(limit).all()
        
        logger.info(f"Trouvé {len(resources)} ressources pour la session {session_id}")
        return resources
        
    except Exception as e:
        logger.error(f"Erreur lors de la recherche des ressources pour la session {session_id}: {str(e)}")
        raise

def get_resources_standalone(db: Session, skip: int = 0, limit: int = 100):
    """Récupère les ressources qui ne sont liées à aucune session."""
    return db.query(Resource).filter(Resource.session_id == None).offset(skip).limit(limit).all()

def create_resource(db: Session, resource: ResourceCreate):
    """Crée une nouvelle ressource."""
    # Vérifier si l'utilisateur existe
    if resource.user_id is not None:
        db_user = db.query(User).filter(User.id == resource.user_id).first()
        if not db_user:
            raise ValueError(f"User with id {resource.user_id} not found")

    # Vérifier si les sessions existent
    if resource.session_ids:
        db_sessions = db.query(Session).filter(Session.id.in_(resource.session_ids)).all()
        if len(db_sessions) != len(resource.session_ids):
            raise ValueError("One or more sessions not found")

    # Créer la ressource
    db_resource = Resource(
        title=resource.title,
        description=resource.description,
        type=resource.type,
        content=resource.content,
        user_id=resource.user_id
    )
    
    # Ajouter la ressource à la base de données
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    
    # Ajouter les relations avec les sessions
    if resource.session_ids:
        for session_id in resource.session_ids:
            db_resource.sessions.append(db.query(Session).get(session_id))
        db.commit()
        db.refresh(db_resource)
    
    # Créer la réponse avec les IDs des sessions
    response_data = {
        "id": db_resource.id,
        "title": db_resource.title,
        "description": db_resource.description,
        "type": db_resource.type,
        "content": db_resource.content,
        "user_id": db_resource.user_id,
        "session_ids": [session.id for session in db_resource.sessions]
    }
    
    return response_data

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

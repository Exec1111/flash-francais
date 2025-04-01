from sqlalchemy.orm import Session
from models import Progression
from schemas.progression import ProgressionCreate, ProgressionUpdate

def get_progression(db: Session, progression_id: int):
    return db.query(Progression).filter(Progression.id == progression_id).first()

def get_progressions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Progression).offset(skip).limit(limit).all()

def create_progression(db: Session, progression: ProgressionCreate):
    db_progression = Progression(**progression.model_dump())
    db.add(db_progression)
    db.commit()
    db.refresh(db_progression)
    return db_progression

def update_progression(db: Session, progression_id: int, progression_update: ProgressionUpdate):
    db_progression = get_progression(db, progression_id=progression_id)
    if db_progression is None:
        return None
    for key, value in progression_update.model_dump(exclude_unset=True).items():
        setattr(db_progression, key, value)
    db.add(db_progression)
    db.commit()
    db.refresh(db_progression)
    return db_progression

def delete_progression(db: Session, progression_id: int):
    db_progression = get_progression(db, progression_id=progression_id)
    if db_progression is None:
        return None
    db.delete(db_progression)
    db.commit()
    return True

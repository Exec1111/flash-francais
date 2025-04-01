from pydantic import BaseModel

class SequenceBase(BaseModel):
    title: str
    description: str | None = None
    progression_id: int

class SequenceCreate(SequenceBase):
    pass

class SequenceUpdate(BaseModel): # Allow partial updates
    title: str | None = None
    description: str | None = None
    progression_id: int | None = None # Usually not updated, but possible

class SequenceRead(SequenceBase):
    id: int
    progression_id: int
    # Inclure potentiellement des sessions ou objectifs liés si nécessaire (attention aux dépendances circulaires)
    # sessions: List["SessionReadSimple"] = [] # Nécessiterait SessionReadSimple
    # objectives: List["ObjectiveReadSimple"] = [] # Nécessiterait ObjectiveReadSimple

    class Config:
        from_attributes = True # Compatible avec l'ORM SQLAlchemy

# Schéma simplifié pour les références (évite dépendances circulaires)
class SequenceReadSimple(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True # Compatible avec l'ORM SQLAlchemy

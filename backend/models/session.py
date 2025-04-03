from sqlalchemy import Column, Integer, String, Text, Interval, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
# Importer la table d'association
from models.association_tables import session_objective_association, session_resource_association

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False)
    notes = Column(Text, nullable=True)
    duration = Column(Interval, nullable=True) # Utilisation de Interval pour la durée
    # Foreign Key to Sequence
    sequence_id = Column(Integer, ForeignKey("sequences.id"), nullable=False)

    # Relationship with Sequence (many-to-one)
    sequence = relationship("Sequence", back_populates="sessions") # 'sessions' sera ajouté à Sequence
    # Relationship with Objective (many-to-many)
    objectives = relationship(
        "Objective",
        secondary=session_objective_association,
        back_populates="sessions"
    )
    
    resources = relationship(
        "Resource",
        secondary=session_resource_association,
        back_populates="sessions"
    )

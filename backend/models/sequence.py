from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
# Importer la table d'association
from models.association_tables import sequence_objective_association

class Sequence(Base):
    __tablename__ = "sequences"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # Foreign Key to Progression
    progression_id = Column(Integer, ForeignKey("progressions.id"), nullable=False)

    # Relationship with Progression (many-to-one)
    progression = relationship("Progression", back_populates="sequences")
    # Relationship with Session (one-to-many)
    sessions = relationship("Session", back_populates="sequence")
    # Relationship with Objective (many-to-many)
    objectives = relationship(
        "Objective",
        secondary=sequence_objective_association,
        back_populates="sequences"
    )

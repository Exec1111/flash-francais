from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class Progression(Base):
    __tablename__ = "progressions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # Relationship with Sequence (one-to-many)
    sequences = relationship("Sequence", back_populates="progression")

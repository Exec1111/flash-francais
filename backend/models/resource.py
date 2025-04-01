from sqlalchemy import Column, Integer, String, Text, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum

# Définir les types de ressources possibles
class ResourceType(str, enum.Enum):
    VIDEO = "video"
    TEXT = "text"
    EXERCISE = "exercise"
    # Ajoutez d'autres types si nécessaire

class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(ResourceType), nullable=False) # Utilisation de l'Enum pour le type
    # Utiliser JSON pour stocker le contenu spécifique au type (URL vidéo, contenu texte, etc.)
    # Ou utiliser Text et analyser côté application.
    # JSON est plus flexible pour différentes structures.
    content = Column(JSON, nullable=True)
    # Foreign Key to Session (Optional)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)

    # Relationship with Session (many-to-one, optional)
    session = relationship("Session", back_populates="resources") # 'resources' sera ajouté à Session

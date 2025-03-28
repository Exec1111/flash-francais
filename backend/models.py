from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    french_word = Column(String(100), nullable=False)
    english_translation = Column(String(100), nullable=False)
    example_sentence = Column(Text)
    difficulty = Column(Integer, default=1)  # Niveau de difficulté de 1 à 5
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

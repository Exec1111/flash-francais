from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FlashcardBase(BaseModel):
    french_word: str
    english_translation: str
    example_sentence: Optional[str] = None
    difficulty: Optional[int] = 1

class FlashcardCreate(FlashcardBase):
    pass

class Flashcard(FlashcardBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

from pydantic import BaseModel, Json
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
import json
import logging

class ResourceBase(BaseModel):
    title: str
    description: Optional[str] = None
    type_id: int
    sub_type_id: int
    content: Optional[Json] = None
    session_ids: Optional[List[int]] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    type_id: int
    sub_type_id: int
    content: Optional[Json] = None
    user_id: int
    type: Optional[Dict] = None
    sub_type: Optional[Dict] = None
    session_ids: List[int]

    @classmethod
    def from_resource(cls, resource, db: Session):
        content_data = None
        if resource.content:
            try:
                content_data = json.loads(resource.content)
            except json.JSONDecodeError:
                logging.error(f"Failed to decode JSON content for resource {resource.id}: {resource.content}")
                content_data = None  

        return cls(
            id=resource.id,
            title=resource.title,
            description=resource.description,
            type_id=resource.type_id,
            sub_type_id=resource.sub_type_id,
            content=content_data,
            user_id=resource.user_id,
            type={
                "id": resource.type.id,
                "key": resource.type.key,
                "value": resource.type.value
            } if resource.type else None,
            sub_type={
                "id": resource.sub_type.id,
                "key": resource.sub_type.key,
                "value": resource.sub_type.value
            } if resource.sub_type else None,
            session_ids=[s.id for s in resource.sessions] if resource.sessions else []
        )

    class Config:
        from_attributes = True
        json_encoders = {
            dict: lambda v: v
        }

class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type_id: Optional[int] = None
    sub_type_id: Optional[int] = None
    content: Optional[Json] = None
    session_ids: Optional[List[int]] = None

    class Config:
        from_attributes = True

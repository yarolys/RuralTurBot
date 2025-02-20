import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class KbButtonSchema(BaseModel):
    id: int
    name: str
    url: HttpUrl


class UserSchema(BaseModel):
    id: int
    full_name: str
    username: Optional[str] = None
    created_at: datetime


class EditableTextSchema(BaseModel):
    id: int
    name_button: str
    identifier: str  
    content: str
    created_at: datetime
    updated_at: datetime


class TourSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AccomodationSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class EntertainmentSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class LocalFoodSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
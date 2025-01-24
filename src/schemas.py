import enum
from datetime import datetime

from pydantic import BaseModel, HttpUrl


class KbButtonSchema(BaseModel):
    id: int
    name: str
    url: HttpUrl


class UserSchema(BaseModel):
    id: int
    full_name: str
    created_at: datetime


class EditableTextSchema(BaseModel):
    id: int
    identifier: str  
    content: str
    created_at: datetime
    updated_at: datetime


from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoomOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    content: str
    room_id: int

class MessageOut(BaseModel):
    id: int
    content: str
    timestamp: datetime
    user_id: int
    room_id: int

    class Config:
        orm_mode = True

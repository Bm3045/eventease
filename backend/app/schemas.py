# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: datetime
    location: Optional[str]
    capacity: int

class BookingOut(BaseModel):
    booking_id: str
    event_id: int
    user_id: int
    created_at: datetime

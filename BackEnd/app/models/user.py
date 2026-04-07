from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    email: str
    created_at: Optional[str] = None

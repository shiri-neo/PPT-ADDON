"""User schemas"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields"""

    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user"""

    password: str


class UserRead(UserBase):
    """Schema for reading user data (response)"""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

"""Organization schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class OrganizationBase(BaseModel):
    """Base organization schema with common fields"""

    name: str


class OrganizationCreate(OrganizationBase):
    """Schema for creating a new organization"""

    pass


class OrganizationRead(BaseModel):
    """Schema for reading organization data (response)"""

    id: int
    name: str
    created_at: datetime
    logo_url: Optional[str] = None
    primary_color: str
    secondary_color: str
    accent_color: str
    font_family: str
    design_style: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationUpdate(BaseModel):
    """Schema for updating organization settings"""

    name: Optional[str] = None
    logo_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    font_family: Optional[str] = None
    design_style: Optional[str] = None


class OrganizationUserRead(BaseModel):
    """Schema for reading organization user information"""

    user_id: int
    email: str
    role: str
    created_at: datetime

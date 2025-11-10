"""Organization schemas"""

from pydantic import BaseModel, ConfigDict


class OrganizationBase(BaseModel):
    """Base organization schema with common fields"""

    name: str


class OrganizationCreate(OrganizationBase):
    """Schema for creating a new organization"""

    pass


class OrganizationRead(OrganizationBase):
    """Schema for reading organization data (response)"""

    id: int

    model_config = ConfigDict(from_attributes=True)

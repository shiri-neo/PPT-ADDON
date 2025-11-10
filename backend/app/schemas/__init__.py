"""Pydantic schemas for request/response validation"""

from app.schemas.auth import Token, LoginRequest, SignupRequest
from app.schemas.user import UserBase, UserCreate, UserRead
from app.schemas.organization import OrganizationBase, OrganizationCreate, OrganizationRead
from app.schemas.document import DocumentRead, DocumentCreateResponse
from app.schemas.presentation import (
    SlideSchema,
    PresentationCreateRequest,
    PresentationRead,
    SlideEditRequest,
    SlideEditResponse,
)
from app.schemas.common import MessageResponse

__all__ = [
    "Token",
    "LoginRequest",
    "SignupRequest",
    "UserBase",
    "UserCreate",
    "UserRead",
    "OrganizationBase",
    "OrganizationCreate",
    "OrganizationRead",
    "DocumentRead",
    "DocumentCreateResponse",
    "SlideSchema",
    "PresentationCreateRequest",
    "PresentationRead",
    "SlideEditRequest",
    "SlideEditResponse",
    "MessageResponse",
]

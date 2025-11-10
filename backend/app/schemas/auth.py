"""Authentication schemas"""

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """JWT token response"""

    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Login request with email and password"""

    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    """Signup request with email and password"""

    email: EmailStr
    password: str

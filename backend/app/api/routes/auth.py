"""Authentication endpoints"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.models.organization import Organization
from app.models.user import UserOrganization
from app.schemas.auth import Token, LoginRequest, SignupRequest
from app.schemas.user import UserRead

router = APIRouter()
settings = get_settings()


@router.post("/signup", response_model=UserRead)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Create a new user account.
    Also creates a default organization for the user.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create new user
    hashed_password = get_password_hash(request.password)
    new_user = User(
        email=request.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.flush()  # Flush to get the user ID

    # Create default organization
    org_name = f"{request.email.split('@')[0]}'s Organization"
    new_org = Organization(name=org_name)
    db.add(new_org)
    db.flush()

    # Link user to organization
    user_org = UserOrganization(
        user_id=new_user.id, organization_id=new_org.id, role="owner"
    )
    db.add(user_org)

    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.jwt_access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

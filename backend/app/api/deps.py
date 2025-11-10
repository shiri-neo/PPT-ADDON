"""API dependencies for dependency injection"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db as _get_db
from app.core.security import get_current_user as _get_current_user
from app.models.user import User
from app.models.organization import Organization


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency"""
    yield from _get_db()


def get_current_user(
    db: Session = Depends(get_db), current_user: User = Depends(_get_current_user)
) -> User:
    """Get current authenticated user dependency"""
    return current_user


def get_current_organization(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Organization:
    """
    Get current user's organization.
    For now, returns the first organization the user belongs to.
    In a real app, this might be selected based on a header or query param.
    """
    if not current_user.organizations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not belong to any organization",
        )

    # Return first organization (stub implementation)
    return current_user.organizations[0]

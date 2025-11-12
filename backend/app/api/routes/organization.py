"""Organization settings and management endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_organization
from app.models.user import User, UserOrganization
from app.models.organization import Organization
from app.schemas.organization import OrganizationRead, OrganizationUpdate, OrganizationUserRead
from app.core.database import get_db

router = APIRouter()


@router.get("/settings", response_model=OrganizationRead)
def get_organization_settings(
    current_org: Organization = Depends(get_current_organization),
):
    """Get current organization settings"""
    return current_org


@router.put("/settings", response_model=OrganizationRead)
def update_organization_settings(
    settings: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    Update organization settings (branding, name, etc.)
    Only admins can update settings
    """
    # Check if user is admin
    user_org = (
        db.query(UserOrganization)
        .filter(
            UserOrganization.user_id == current_user.id,
            UserOrganization.organization_id == current_org.id,
        )
        .first()
    )

    if not user_org or user_org.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update organization settings",
        )

    # Update organization fields
    if settings.name is not None:
        current_org.name = settings.name
    if settings.primary_color is not None:
        current_org.primary_color = settings.primary_color
    if settings.secondary_color is not None:
        current_org.secondary_color = settings.secondary_color
    if settings.accent_color is not None:
        current_org.accent_color = settings.accent_color
    if settings.font_family is not None:
        current_org.font_family = settings.font_family
    if settings.design_style is not None:
        current_org.design_style = settings.design_style
    if settings.logo_url is not None:
        current_org.logo_url = settings.logo_url

    db.commit()
    db.refresh(current_org)

    return current_org


@router.get("/users", response_model=List[OrganizationUserRead])
def list_organization_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """List all users in the organization"""
    user_orgs = (
        db.query(UserOrganization, User)
        .join(User, UserOrganization.user_id == User.id)
        .filter(UserOrganization.organization_id == current_org.id)
        .all()
    )

    result = []
    for user_org, user in user_orgs:
        result.append(
            OrganizationUserRead(
                user_id=user.id,
                email=user.email,
                role=user_org.role,
                created_at=user.created_at,
            )
        )

    return result


@router.post("/users/invite")
def invite_user_to_organization(
    email: str,
    role: str = "member",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    Invite a user to the organization
    Only admins can invite users
    TODO: Send invitation email
    """
    # Check if current user is admin
    user_org = (
        db.query(UserOrganization)
        .filter(
            UserOrganization.user_id == current_user.id,
            UserOrganization.organization_id == current_org.id,
        )
        .first()
    )

    if not user_org or user_org.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can invite users",
        )

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        # Check if already in organization
        existing_membership = (
            db.query(UserOrganization)
            .filter(
                UserOrganization.user_id == existing_user.id,
                UserOrganization.organization_id == current_org.id,
            )
            .first()
        )

        if existing_membership:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a member of this organization",
            )

        # Add to organization
        new_membership = UserOrganization(
            user_id=existing_user.id,
            organization_id=current_org.id,
            role=role,
        )
        db.add(new_membership)
        db.commit()

        return {"message": f"User {email} added to organization", "user_id": existing_user.id}

    # TODO: Send invitation email for new users
    return {"message": f"Invitation sent to {email} (email sending not yet implemented)"}


@router.delete("/users/{user_id}")
def remove_user_from_organization(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    Remove a user from the organization
    Only admins can remove users
    """
    # Check if current user is admin
    user_org = (
        db.query(UserOrganization)
        .filter(
            UserOrganization.user_id == current_user.id,
            UserOrganization.organization_id == current_org.id,
        )
        .first()
    )

    if not user_org or user_org.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can remove users",
        )

    # Cannot remove yourself
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot remove yourself from the organization",
        )

    # Find and delete membership
    membership = (
        db.query(UserOrganization)
        .filter(
            UserOrganization.user_id == user_id,
            UserOrganization.organization_id == current_org.id,
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in organization",
        )

    db.delete(membership)
    db.commit()

    return {"message": "User removed from organization"}


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    new_role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    Update a user's role in the organization
    Only admins can update roles
    """
    # Check if current user is admin
    user_org = (
        db.query(UserOrganization)
        .filter(
            UserOrganization.user_id == current_user.id,
            UserOrganization.organization_id == current_org.id,
        )
        .first()
    )

    if not user_org or user_org.role not in ["admin", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update user roles",
        )

    # Find membership
    membership = (
        db.query(UserOrganization)
        .filter(
            UserOrganization.user_id == user_id,
            UserOrganization.organization_id == current_org.id,
        )
        .first()
    )

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in organization",
        )

    # Update role
    membership.role = new_role
    db.commit()

    return {"message": f"User role updated to {new_role}"}

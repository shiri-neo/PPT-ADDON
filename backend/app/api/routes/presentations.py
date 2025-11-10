"""Presentation generation and editing endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_organization
from app.models.user import User
from app.models.organization import Organization
from app.models.document import Document
from app.models.presentation import Slide
from app.schemas.presentation import (
    PresentationCreateRequest,
    PresentationRead,
    SlideEditRequest,
    SlideEditResponse,
    SlideSchema,
)
from app.services.presentations import (
    create_presentation_from_document,
    edit_presentation_slide,
)

router = APIRouter()


@router.post("/from-document", response_model=PresentationRead)
def generate_presentation_from_document(
    request: PresentationCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    Generate a presentation from a document using AI (stubbed).
    Creates presentation and slides in the database.
    """
    # Verify document exists and belongs to organization
    document = (
        db.query(Document)
        .filter(
            Document.id == request.document_id,
            Document.organization_id == current_org.id,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # Create presentation with slides
    presentation = create_presentation_from_document(
        document=document,
        slide_count=request.slide_count,
        tone=request.tone,
        organization_id=current_org.id,
        db=db,
    )

    # Build response with slides
    slides_data = [
        SlideSchema(
            title=slide.title,
            bullets=slide.bullets,
            notes=slide.notes,
        )
        for slide in presentation.slides
    ]

    return PresentationRead(
        id=presentation.id,
        title=presentation.title,
        created_at=presentation.created_at,
        slides=slides_data,
    )


@router.post("/{presentation_id}/slides/{index}/edit", response_model=SlideEditResponse)
def edit_slide(
    presentation_id: int,
    index: int,
    request: SlideEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    Edit a specific slide using natural language instruction.
    Uses AI to modify slide content (stubbed).
    """
    # Find slide
    slide = (
        db.query(Slide)
        .join(Slide.presentation)
        .filter(
            Slide.presentation_id == presentation_id,
            Slide.index == index,
        )
        .first()
    )

    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Slide at index {index} not found in presentation {presentation_id}",
        )

    # Verify presentation belongs to organization
    if slide.presentation.organization_id != current_org.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    # Edit slide
    updated_slide = edit_presentation_slide(
        slide=slide,
        instruction=request.instruction,
        db=db,
    )

    return SlideEditResponse(
        slide=SlideSchema(
            title=updated_slide.title,
            bullets=updated_slide.bullets,
            notes=updated_slide.notes,
        )
    )

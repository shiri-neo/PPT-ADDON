"""Presentation generation and editing endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_organization
from app.models.user import User
from app.models.organization import Organization
from app.models.document import Document
from app.models.presentation import Presentation, Slide
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
from app.services.pptx_generator import generate_pptx_file

router = APIRouter()


@router.get("", response_model=List[PresentationRead])
def list_presentations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    List all presentations for the current organization.
    """
    presentations = (
        db.query(Presentation)
        .filter(Presentation.organization_id == current_org.id)
        .order_by(Presentation.created_at.desc())
        .all()
    )

    # Build response with slides for each presentation
    result = []
    for presentation in presentations:
        slides_data = [
            SlideSchema(
                title=slide.title,
                bullets=slide.bullets,
                notes=slide.notes,
            )
            for slide in presentation.slides
        ]
        result.append(
            PresentationRead(
                id=presentation.id,
                title=presentation.title,
                created_at=presentation.created_at,
                slides=slides_data,
            )
        )

    return result


@router.get("/{presentation_id}/download")
def download_presentation(
    presentation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_organization),
):
    """
    Download a presentation as a PowerPoint file.
    """
    # Find presentation
    presentation = (
        db.query(Presentation)
        .filter(
            Presentation.id == presentation_id,
            Presentation.organization_id == current_org.id,
        )
        .first()
    )

    if not presentation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Presentation not found",
        )

    # Generate PPTX file with company branding
    pptx_file = generate_pptx_file(presentation, organization=current_org)

    # Create safe filename
    safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in presentation.title)
    filename = f"{safe_title}.pptx"

    # Return as streaming response
    return StreamingResponse(
        pptx_file,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


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

    # Create presentation with slides using AI and company branding
    presentation = create_presentation_from_document(
        document=document,
        slide_count=request.slide_count,
        tone=request.tone,
        organization_id=current_org.id,
        custom_instructions=request.custom_instructions,
        organization=current_org,
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

"""Presentation service for generating and editing slides"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.presentation import Presentation, Slide
from app.schemas.presentation import SlideSchema
from app.services.llm import generate_presentation_from_document, edit_slide_content


def create_presentation_from_document(
    document: Document,
    slide_count: int,
    tone: Optional[str],
    organization_id: int,
    custom_instructions: Optional[str],
    organization,
    db: Session,
) -> Presentation:
    """
    Create a presentation from a document using AI with company branding.

    Args:
        document: Source document
        slide_count: Number of slides to generate
        tone: Presentation tone (formal, casual, etc.)
        organization_id: Organization ID
        custom_instructions: User's specific instructions
        organization: Organization model (for branding)
        db: Database session

    Returns:
        Created Presentation object with slides
    """
    # Prepare company branding
    company_branding = {
        "primary_color": organization.primary_color,
        "secondary_color": organization.secondary_color,
        "accent_color": organization.accent_color,
        "design_style": organization.design_style,
        "font_family": organization.font_family,
    }

    # Generate slides using LLM with AI analysis and branding
    slides_data = generate_presentation_from_document(
        document_text=document.parsed_text or "",
        slide_count=slide_count,
        tone=tone,
        custom_instructions=custom_instructions,
        company_branding=company_branding,
        document_name=document.name,
    )

    # Create presentation
    presentation_title = f"Presentation from {document.name}"
    presentation = Presentation(
        organization_id=organization_id,
        document_id=document.id,
        title=presentation_title,
        meta={"slide_count": slide_count, "tone": tone},
    )
    db.add(presentation)
    db.flush()  # Get presentation ID

    # Create slides
    for idx, slide_data in enumerate(slides_data):
        slide = Slide(
            presentation_id=presentation.id,
            index=idx,
            title=slide_data.title,
            bullets=slide_data.bullets,
            notes=slide_data.notes,
        )
        db.add(slide)

    db.commit()
    db.refresh(presentation)

    return presentation


def edit_presentation_slide(
    slide: Slide,
    instruction: str,
    db: Session,
) -> Slide:
    """
    Edit a presentation slide based on instruction using AI.

    Args:
        slide: Slide to edit
        instruction: Natural language editing instruction
        db: Database session

    Returns:
        Updated Slide object
    """
    # Create SlideSchema from current slide
    current_slide_data = SlideSchema(
        title=slide.title,
        bullets=slide.bullets,
        notes=slide.notes,
    )

    # Edit slide using LLM (stubbed)
    edited_slide_data = edit_slide_content(current_slide_data, instruction)

    # Update slide in database
    slide.title = edited_slide_data.title
    slide.bullets = edited_slide_data.bullets
    slide.notes = edited_slide_data.notes

    db.commit()
    db.refresh(slide)

    return slide

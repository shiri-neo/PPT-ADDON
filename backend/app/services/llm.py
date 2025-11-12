"""AI/LLM service for content generation using OpenAI (with stubbed responses)"""

from typing import List, Optional, Dict
import asyncio

from app.schemas.presentation import SlideSchema
from app.core.config import get_settings
from app.services.ai_service import ai_service

settings = get_settings()

# TODO: Initialize OpenAI client when ready
# import openai
# openai.api_key = settings.openai_api_key


def generate_presentation_from_document(
    document_text: str,
    slide_count: int,
    tone: Optional[str] = None,
    custom_instructions: Optional[str] = None,
    company_branding: Optional[Dict[str, str]] = None,
    document_name: Optional[str] = "Uploaded Document"
) -> List[SlideSchema]:
    """
    Generate presentation slides from document text using AI.

    Args:
        document_text: The parsed text from the document
        slide_count: Number of slides to generate
        tone: Optional tone (formal, casual, marketing, academic)
        custom_instructions: User's specific instructions for the presentation
        company_branding: Company branding settings (colors, style, logo)
        document_name: Name of the source document

    Returns:
        List of SlideSchema objects

    TODO: This uses the AI service with stubbed responses. When ready to use real OpenAI:
          1. Set OPENAI_API_KEY in .env
          2. Uncomment OpenAI initialization in ai_service.py
          3. The stubbed responses will be replaced with real AI-generated content
    """
    # Default branding if not provided
    if not company_branding:
        company_branding = {
            "primary_color": "#0078D4",
            "secondary_color": "#106EBE",
            "accent_color": "#00BCF2",
            "design_style": "professional",
            "font_family": "Arial"
        }

    # Step 1: Analyze the document using AI
    analysis = asyncio.run(ai_service.analyze_document(
        document_content=document_text,
        document_name=document_name,
        custom_instructions=custom_instructions
    ))

    # Step 2: Generate presentation structure using AI
    slides_data = asyncio.run(ai_service.generate_presentation_structure(
        analysis=analysis,
        slide_count=slide_count,
        tone=tone or "professional",
        company_branding=company_branding,
        custom_instructions=custom_instructions
    ))

    # Step 3: Convert to SlideSchema objects
    slides = []
    for slide_data in slides_data:
        slides.append(SlideSchema(
            title=slide_data["title"],
            bullets=slide_data["bullets"],
            notes=slide_data.get("notes", "")
        ))

    return slides


def edit_slide_content(slide: SlideSchema, instruction: str) -> SlideSchema:
    """
    Edit slide content based on natural language instruction using AI.

    Args:
        slide: The current slide data
        instruction: Natural language instruction for editing

    Returns:
        Updated SlideSchema

    TODO: This uses the AI service with stubbed responses. Real OpenAI will refine based on instruction.
    """
    # Convert SlideSchema to dict for AI service
    slide_dict = {
        "title": slide.title,
        "bullets": slide.bullets,
        "notes": slide.notes
    }

    # Use AI service to refine slide
    edited_slide = asyncio.run(ai_service.refine_slide_content(
        slide_content=slide_dict,
        instruction=instruction
    ))

    return SlideSchema(
        title=edited_slide["title"],
        bullets=edited_slide["bullets"],
        notes=edited_slide.get("notes", "")
    )

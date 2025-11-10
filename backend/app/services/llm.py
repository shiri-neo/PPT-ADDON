"""AI/LLM service for content generation (stubbed with fake data)"""

from typing import List, Optional

from app.schemas.presentation import SlideSchema
from app.core.config import get_settings

settings = get_settings()

# TODO: Initialize OpenAI client when ready
# import openai
# openai.api_key = settings.openai_api_key


def generate_presentation_from_document(
    document_text: str, slide_count: int, tone: Optional[str] = None
) -> List[SlideSchema]:
    """
    Generate presentation slides from document text using AI.

    Args:
        document_text: The parsed text from the document
        slide_count: Number of slides to generate
        tone: Optional tone (formal, casual, marketing, academic)

    Returns:
        List of SlideSchema objects

    TODO: Implement actual OpenAI API call
    """
    # TODO: Call OpenAI API to generate slides
    # Example:
    # prompt = f"Create {slide_count} presentation slides from this document with a {tone} tone:\n\n{document_text}"
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # Parse response and convert to SlideSchema objects

    # STUB: Return fake slides
    fake_slides = [
        SlideSchema(
            title="Introduction",
            bullets=[
                "Welcome to the presentation",
                "Overview of key topics",
                "What you'll learn today",
            ],
            notes="This is an introductory slide generated from your document.",
        ),
        SlideSchema(
            title="Main Points",
            bullets=[
                "First major concept from document",
                "Second key insight",
                "Third important detail",
                "Supporting evidence",
            ],
            notes="These points were extracted from the document content.",
        ),
        SlideSchema(
            title="Conclusion",
            bullets=[
                "Summary of key takeaways",
                "Next steps and actions",
                "Questions and discussion",
            ],
            notes="Concluding thoughts and call to action.",
        ),
    ]

    # Return the requested number of slides (or all fake slides if less)
    return fake_slides[:slide_count]


def edit_slide_content(slide: SlideSchema, instruction: str) -> SlideSchema:
    """
    Edit slide content based on natural language instruction using AI.

    Args:
        slide: The current slide data
        instruction: Natural language instruction for editing

    Returns:
        Updated SlideSchema

    TODO: Implement actual OpenAI API call
    """
    # TODO: Call OpenAI API to edit slide
    # Example:
    # prompt = f"Edit this slide based on the instruction.\n\nSlide:\nTitle: {slide.title}\nBullets: {slide.bullets}\n\nInstruction: {instruction}"
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # Parse response and update slide

    # STUB: Return slide with "(edited)" appended
    edited_title = f"{slide.title} (edited)"
    edited_bullets = [f"{bullet} (edited)" for bullet in slide.bullets]
    edited_notes = (
        f"{slide.notes} (edited by: {instruction})" if slide.notes else instruction
    )

    return SlideSchema(
        title=edited_title,
        bullets=edited_bullets,
        notes=edited_notes,
    )

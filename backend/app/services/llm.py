"""AI/LLM service for content generation using OpenAI with DALL-E image generation"""

from typing import List, Optional, Dict
import asyncio

from app.schemas.presentation import SlideSchema
from app.core.config import get_settings
from app.services.ai_service import ai_service

settings = get_settings()


async def generate_images_for_slides(slides_data: List[Dict]) -> List[Dict]:
    """
    Generate AI images for each slide using DALL-E.

    Args:
        slides_data: List of slide dictionaries with image_prompt and image_style

    Returns:
        Same slides_data with image_url added to each slide
    """
    print(f"\n🎨 Generating {len(slides_data)} AI images with DALL-E...")

    # Generate images concurrently for better performance
    async def generate_image_for_slide(slide_data: Dict, index: int) -> Dict:
        image_prompt = slide_data.get("image_prompt", "")
        image_style = slide_data.get("image_style", "professional")
        slide_title = slide_data.get("title", "")

        if image_prompt:
            image_url = await ai_service.generate_slide_image(
                image_prompt=image_prompt,
                image_style=image_style,
                slide_title=slide_title
            )
            slide_data["image_url"] = image_url
            print(f"  [{index + 1}/{len(slides_data)}] {'✅' if image_url else '⚠️ '} {slide_title[:50]}")
        else:
            slide_data["image_url"] = None
            print(f"  [{index + 1}/{len(slides_data)}] ⏭️  Skipped: {slide_title[:50]}")

        return slide_data

    # Generate all images in parallel (but limit concurrency to avoid rate limits)
    tasks = [generate_image_for_slide(slide, idx) for idx, slide in enumerate(slides_data)]
    enhanced_slides = await asyncio.gather(*tasks)

    success_count = sum(1 for slide in enhanced_slides if slide.get("image_url"))
    print(f"✅ Generated {success_count}/{len(enhanced_slides)} images successfully\n")

    return enhanced_slides


def generate_presentation_from_document(
    document_text: str,
    slide_count: int,
    tone: Optional[str] = None,
    custom_instructions: Optional[str] = None,
    company_branding: Optional[Dict[str, str]] = None,
    document_name: Optional[str] = "Uploaded Document"
) -> List[SlideSchema]:
    """
    Generate presentation slides from document text using AI with personalized images.

    This function:
    1. Analyzes the document with GPT-4 to extract key information
    2. Generates a personalized presentation structure with GPT-4
    3. Creates unique AI-generated images for each slide using DALL-E 3
    4. Returns fully structured slides ready for PowerPoint generation

    Args:
        document_text: The parsed text from the document
        slide_count: Number of slides to generate
        tone: Optional tone (formal, casual, marketing, academic)
        custom_instructions: User's specific instructions for the presentation
        company_branding: Company branding settings (colors, style, logo)
        document_name: Name of the source document

    Returns:
        List of SlideSchema objects with embedded image URLs

    Note: If OPENAI_API_KEY is not configured, returns stub responses without images
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

    print(f"\n🤖 Generating AI-powered presentation from '{document_name}'...")
    print(f"   Settings: {slide_count} slides, {tone or 'professional'} tone")
    if custom_instructions:
        print(f"   Custom instructions: {custom_instructions[:100]}...")

    # Step 1: Analyze the document using GPT-4
    print("\n📖 Step 1: Analyzing document with GPT-4...")
    analysis = asyncio.run(ai_service.analyze_document(
        document_content=document_text,
        document_name=document_name,
        custom_instructions=custom_instructions
    ))
    print(f"   Topics identified: {len(analysis.get('main_topics', []))}")

    # Step 2: Generate presentation structure using GPT-4
    print("\n✨ Step 2: Generating personalized presentation structure with GPT-4...")
    slides_data = asyncio.run(ai_service.generate_presentation_structure(
        analysis=analysis,
        slide_count=slide_count,
        tone=tone or "professional",
        company_branding=company_branding,
        custom_instructions=custom_instructions
    ))
    print(f"   Created {len(slides_data)} slides")

    # Step 3: Generate AI images for each slide using DALL-E 3
    print("\n🎨 Step 3: Generating unique AI images for each slide with DALL-E 3...")
    slides_with_images = asyncio.run(generate_images_for_slides(slides_data))

    # Step 4: Convert to SlideSchema objects with metadata
    print("\n📦 Step 4: Packaging slides with metadata...")
    slides = []
    for slide_data in slides_with_images:
        # Create slide with image URL in metadata
        slide = SlideSchema(
            title=slide_data["title"],
            bullets=slide_data["bullets"],
            notes=slide_data.get("notes", "")
        )
        # Store image URL in a way the PPTX generator can access it
        # We'll add a metadata field to SlideSchema
        if hasattr(slide, '__dict__'):
            slide.__dict__['_image_url'] = slide_data.get("image_url")

        slides.append(slide)

    print(f"\n✅ Presentation generation complete! {len(slides)} slides ready.\n")
    return slides


def edit_slide_content(slide: SlideSchema, instruction: str) -> SlideSchema:
    """
    Edit slide content based on natural language instruction using GPT-4.

    Args:
        slide: The current slide data
        instruction: Natural language instruction for editing

    Returns:
        Updated SlideSchema

    Note: If OPENAI_API_KEY is not configured, returns modified stub response
    """
    print(f"\n✏️  Editing slide: '{slide.title[:50]}...'")
    print(f"   Instruction: {instruction}")

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

    result = SlideSchema(
        title=edited_slide["title"],
        bullets=edited_slide["bullets"],
        notes=edited_slide.get("notes", "")
    )

    print(f"✅ Slide edited successfully\n")
    return result

"""PowerPoint file generation service with company branding and AI-generated images"""

from io import BytesIO
from typing import List, Optional
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

from app.models.presentation import Presentation as PresentationModel


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def download_image(url: str, timeout: int = 30) -> Optional[BytesIO]:
    """
    Download an image from a URL and return as BytesIO.

    Args:
        url: Image URL
        timeout: Request timeout in seconds

    Returns:
        BytesIO containing image data, or None if download fails
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            print(f"❌ Failed to download image: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error downloading image from {url}: {e}")
        return None


def generate_pptx_file(presentation: PresentationModel, organization=None) -> BytesIO:
    """
    Generate a PowerPoint file from a presentation model with company branding and AI images.

    Args:
        presentation: Presentation model with slides
        organization: Organization model with branding settings (optional)

    Returns:
        BytesIO object containing the PPTX file
    """
    # Create a presentation object
    prs = Presentation()

    # Set slide width and height (standard 16:9)
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    # Extract branding colors
    if organization:
        primary_rgb = hex_to_rgb(organization.primary_color)
        secondary_rgb = hex_to_rgb(organization.secondary_color)
        accent_rgb = hex_to_rgb(organization.accent_color)
        font_name = organization.font_family
        logo_url = organization.logo_url
    else:
        primary_rgb = (0, 120, 212)  # Default blue
        secondary_rgb = (16, 110, 190)
        accent_rgb = (0, 188, 242)
        font_name = "Arial"
        logo_url = None

    # Download logo once if available
    logo_stream = None
    if logo_url:
        print(f"📥 Downloading company logo from {logo_url}")
        logo_stream = download_image(logo_url)
        if logo_stream:
            print("✅ Logo downloaded successfully")

    # Add slides from the presentation model
    for idx, slide_model in enumerate(presentation.slides):
        # Add a blank slide
        blank_slide_layout = prs.slide_layouts[6]  # Blank layout
        slide = prs.slides.add_slide(blank_slide_layout)

        # Check if slide has an AI-generated image
        slide_meta = slide_model.get_meta()  # Assuming slide_model has a meta field for image_url
        image_url = slide_meta.get('image_url') if isinstance(slide_meta, dict) else None
        has_image = image_url is not None

        # Add colored header bar at top
        header_shape = slide.shapes.add_shape(
            1,  # Rectangle
            Inches(0), Inches(0),
            Inches(10), Inches(0.3)
        )
        header_fill = header_shape.fill
        header_fill.solid()
        header_fill.fore_color.rgb = RGBColor(*primary_rgb)

        # Add logo if available (top right corner of first slide)
        if logo_stream and idx == 0:
            try:
                logo_stream.seek(0)  # Reset stream position
                slide.shapes.add_picture(
                    logo_stream,
                    Inches(8.5),   # left
                    Inches(0.4),   # top
                    height=Inches(0.5)
                )
                print(f"✅ Logo added to slide {idx + 1}")
            except Exception as e:
                print(f"❌ Error adding logo to slide {idx + 1}: {e}")

        # Layout depends on whether we have an image
        if has_image:
            # Layout with image on the right side
            title_width = Inches(5.5)
            content_width = Inches(4.5)
            content_left = Inches(0.5)
            image_left = Inches(5.5)
            image_top = Inches(1.0)
            image_width = Inches(4.0)
            image_height = Inches(4.0)
        else:
            # Full-width layout
            title_width = Inches(9)
            content_width = Inches(9)
            content_left = Inches(0.5)

        # Add title with company primary color
        title_box = slide.shapes.add_textbox(
            Inches(0.5),    # left
            Inches(0.5),    # top
            title_width,    # width
            Inches(0.8)     # height
        )
        title_frame = title_box.text_frame
        title_frame.text = slide_model.title
        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(32 if idx == 0 else 28)  # Larger title for first slide
        title_para.font.bold = True
        title_para.font.name = font_name
        title_para.font.color.rgb = RGBColor(*primary_rgb)

        # Add AI-generated image if available
        if has_image:
            print(f"🎨 Downloading AI-generated image for slide {idx + 1}")
            image_stream = download_image(image_url)
            if image_stream:
                try:
                    slide.shapes.add_picture(
                        image_stream,
                        image_left,
                        image_top,
                        width=image_width,
                        height=image_height
                    )
                    print(f"✅ AI image added to slide {idx + 1}")
                except Exception as e:
                    print(f"❌ Error adding AI image to slide {idx + 1}: {e}")
            else:
                print(f"⚠️  Could not download AI image for slide {idx + 1}")

        # Add bullets with company font and accent color
        if slide_model.bullets:
            bullets_box = slide.shapes.add_textbox(
                content_left,    # left
                Inches(1.6),     # top
                content_width,   # width
                Inches(3.5)      # height
            )
            text_frame = bullets_box.text_frame
            text_frame.word_wrap = True

            for i, bullet_text in enumerate(slide_model.bullets):
                if i == 0:
                    p = text_frame.paragraphs[0]
                else:
                    p = text_frame.add_paragraph()

                p.text = bullet_text
                p.level = 0
                p.font.size = Pt(18)
                p.font.name = font_name
                p.font.color.rgb = RGBColor(50, 50, 50)  # Dark gray for readability
                p.space_before = Pt(6)

        # Add footer bar with accent color
        footer_shape = slide.shapes.add_shape(
            1,  # Rectangle
            Inches(0), Inches(5.325),
            Inches(10), Inches(0.3)
        )
        footer_fill = footer_shape.fill
        footer_fill.solid()
        footer_fill.fore_color.rgb = RGBColor(*accent_rgb)

        # Add slide number in footer
        slide_num_box = slide.shapes.add_textbox(
            Inches(9.2), Inches(5.35),
            Inches(0.6), Inches(0.25)
        )
        slide_num_frame = slide_num_box.text_frame
        slide_num_frame.text = str(idx + 1)
        slide_num_para = slide_num_frame.paragraphs[0]
        slide_num_para.font.size = Pt(10)
        slide_num_para.font.color.rgb = RGBColor(255, 255, 255)
        slide_num_para.alignment = PP_ALIGN.RIGHT

        # Add notes if available
        if slide_model.notes:
            notes_slide = slide.notes_slide
            notes_text_frame = notes_slide.notes_text_frame
            notes_text_frame.text = slide_model.notes

    # Save to BytesIO
    pptx_file = BytesIO()
    prs.save(pptx_file)
    pptx_file.seek(0)

    return pptx_file

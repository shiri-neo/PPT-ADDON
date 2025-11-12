"""PowerPoint file generation service with company branding support"""

from io import BytesIO
from typing import List, Optional
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from app.models.presentation import Presentation as PresentationModel

# TODO: Add 'import requests' when implementing logo download from URL


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def generate_pptx_file(presentation: PresentationModel, organization=None) -> BytesIO:
    """
    Generate a PowerPoint file from a presentation model with company branding.

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
        has_logo = organization.logo_url is not None
    else:
        primary_rgb = (0, 120, 212)  # Default blue
        secondary_rgb = (16, 110, 190)
        accent_rgb = (0, 188, 242)
        font_name = "Arial"
        has_logo = False

    # Add slides from the presentation model
    for idx, slide_model in enumerate(presentation.slides):
        # Add a blank slide
        blank_slide_layout = prs.slide_layouts[6]  # Blank layout
        slide = prs.slides.add_slide(blank_slide_layout)

        # Add colored header bar at top
        header_shape = slide.shapes.add_shape(
            1,  # Rectangle
            Inches(0), Inches(0),
            Inches(10), Inches(0.3)
        )
        header_fill = header_shape.fill
        header_fill.solid()
        header_fill.fore_color.rgb = RGBColor(*primary_rgb)

        # Add logo if available (top right corner)
        if has_logo and idx == 0:  # Logo on first slide
            # TODO: Download and add logo image
            # logo_response = requests.get(organization.logo_url)
            # if logo_response.status_code == 200:
            #     logo_stream = BytesIO(logo_response.content)
            #     slide.shapes.add_picture(logo_stream, Inches(8.5), Inches(0.4), height=Inches(0.5))
            pass

        # Add title with company primary color
        title_box = slide.shapes.add_textbox(
            Inches(0.5),    # left
            Inches(0.5),    # top
            Inches(9),      # width
            Inches(0.8)     # height
        )
        title_frame = title_box.text_frame
        title_frame.text = slide_model.title
        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(32)
        title_para.font.bold = True
        title_para.font.name = font_name
        title_para.font.color.rgb = RGBColor(*primary_rgb)

        # Add bullets with company font and accent color
        if slide_model.bullets:
            bullets_box = slide.shapes.add_textbox(
                Inches(0.5),    # left
                Inches(1.6),    # top
                Inches(9),      # width
                Inches(3.5)     # height
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

"""PowerPoint file generation service"""

from io import BytesIO
from typing import List
from pptx import Presentation
from pptx.util import Inches, Pt

from app.models.presentation import Presentation as PresentationModel


def generate_pptx_file(presentation: PresentationModel) -> BytesIO:
    """
    Generate a PowerPoint file from a presentation model.

    Args:
        presentation: Presentation model with slides

    Returns:
        BytesIO object containing the PPTX file
    """
    # Create a presentation object
    prs = Presentation()

    # Set slide width and height (standard 16:9)
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    # Add slides from the presentation model
    for slide_model in presentation.slides:
        # Add a blank slide
        blank_slide_layout = prs.slide_layouts[6]  # Blank layout
        slide = prs.slides.add_slide(blank_slide_layout)

        # Add title
        title_box = slide.shapes.add_textbox(
            Inches(0.5),    # left
            Inches(0.4),    # top
            Inches(9),      # width
            Inches(0.8)     # height
        )
        title_frame = title_box.text_frame
        title_frame.text = slide_model.title
        title_frame.paragraphs[0].font.size = Pt(32)
        title_frame.paragraphs[0].font.bold = True

        # Add bullets
        if slide_model.bullets:
            bullets_box = slide.shapes.add_textbox(
                Inches(0.5),    # left
                Inches(1.5),    # top
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
                # Add bullet point
                p.space_before = Pt(6)

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

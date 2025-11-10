"""Presentation and slide schemas"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class SlideSchema(BaseModel):
    """Schema for a single slide"""

    title: str
    bullets: List[str]
    notes: Optional[str] = None


class PresentationCreateRequest(BaseModel):
    """Request schema for creating a presentation from a document"""

    document_id: int
    slide_count: int = 5
    tone: Optional[str] = None  # formal, casual, marketing, academic, etc.


class PresentationRead(BaseModel):
    """Schema for reading presentation data (response)"""

    id: int
    title: str
    created_at: datetime
    slides: List[SlideSchema]

    model_config = ConfigDict(from_attributes=True)


class SlideEditRequest(BaseModel):
    """Request schema for editing a slide"""

    instruction: str  # Natural language instruction for editing


class SlideEditResponse(BaseModel):
    """Response schema after editing a slide"""

    slide: SlideSchema
    message: str = "Slide updated successfully"

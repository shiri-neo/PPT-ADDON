"""Presentation and Slide models"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Presentation(Base):
    """Presentation model for generated slide decks"""

    __tablename__ = "presentations"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    document_id = Column(
        Integer, ForeignKey("documents.id"), nullable=True
    )  # Source document (optional)
    title = Column(String, nullable=False)
    meta = Column(JSON, nullable=True)  # Additional metadata (tone, settings, etc.)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="presentations")
    document = relationship("Document", back_populates="presentations")
    slides = relationship(
        "Slide", back_populates="presentation", order_by="Slide.index"
    )


class Slide(Base):
    """Slide model for individual slides within a presentation"""

    __tablename__ = "slides"

    id = Column(Integer, primary_key=True, index=True)
    presentation_id = Column(Integer, ForeignKey("presentations.id"), nullable=False)
    index = Column(Integer, nullable=False)  # Slide order/position (0-indexed)
    title = Column(String, nullable=False)
    bullets = Column(JSON, nullable=False)  # List of bullet points as JSON array
    notes = Column(Text, nullable=True)  # Speaker notes
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    presentation = relationship("Presentation", back_populates="slides")

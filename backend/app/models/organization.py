"""Organization model"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organization(Base):
    """Organization model for multi-tenancy"""

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Company branding settings
    logo_url = Column(String, nullable=True)  # URL to company logo
    primary_color = Column(String(7), default="#0078D4", nullable=False)  # Hex color
    secondary_color = Column(String(7), default="#106EBE", nullable=False)  # Hex color
    accent_color = Column(String(7), default="#00BCF2", nullable=False)  # Hex color
    font_family = Column(String, default="Arial", nullable=False)  # Font name
    design_style = Column(String, default="professional", nullable=False)  # professional, modern, creative, minimal

    # Relationships
    users = relationship(
        "User",
        secondary="user_organizations",
        back_populates="organizations",
    )
    documents = relationship("Document", back_populates="organization")
    presentations = relationship("Presentation", back_populates="organization")


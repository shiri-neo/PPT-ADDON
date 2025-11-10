"""Document model for uploaded files"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Document(Base):
    """Document model for storing uploaded file metadata and parsed content"""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)  # S3 object key (stubbed for now)
    parsed_text = Column(Text, nullable=True)  # Extracted/parsed text content
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="documents")
    presentations = relationship("Presentation", back_populates="document")

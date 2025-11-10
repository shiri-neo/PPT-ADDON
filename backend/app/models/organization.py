"""Organization model"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organization(Base):
    """Organization model for multi-tenancy"""

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    users = relationship(
        "User",
        secondary="user_organizations",
        back_populates="organizations",
    )
    documents = relationship("Document", back_populates="organization")
    presentations = relationship("Presentation", back_populates="organization")

"""Document schemas"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentRead(BaseModel):
    """Schema for reading document data (response)"""

    id: int
    name: str
    original_filename: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentCreateResponse(BaseModel):
    """Response after creating a document"""

    document: DocumentRead
    message: str = "Document uploaded successfully"

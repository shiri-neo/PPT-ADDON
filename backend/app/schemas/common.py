"""Common schemas used across the application"""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Generic message response"""

    message: str

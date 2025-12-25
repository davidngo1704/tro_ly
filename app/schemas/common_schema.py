"""Common schema definitions.

Provides shared Pydantic models for API request/response validation.
"""

from pydantic import BaseModel


class ChatModel(BaseModel):
    """Schema for chat requests.
    
    Attributes:
        message (str): User message content.
    """
    message: str
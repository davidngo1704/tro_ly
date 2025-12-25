"""data schema module.

Defines Pydantic schemas for data data validation and serialization.
"""

from pydantic import BaseModel

class dataCreate(BaseModel):
    """Schema for creating a new data.
    
    Attributes:
        code (str): data code identifier.
        name (str): data name.
        type (str): data type classification.
        description (str): Detailed description of the data.
    """
    code: str
    name: str
    type: str
    description: str
    value: str

class dataUpdate(BaseModel):
    """Schema for updating an existing data.
    
    All fields are optional to support partial updates.
    
    Attributes:
        code (str | None): data code identifier.
        name (str | None): data name.
        type (str | None): data type classification.
        description (str | None): Detailed description of the data.
    """
    code: str | None
    name: str | None
    type: str | None
    description: str | None
    value: str | None


class dataResponse(BaseModel):
    """Schema for data API responses.
    
    Attributes:
        id (int): Unique data identifier.
        code (str): data code identifier.
        name (str): data name.
        type (str): data type classification.
        description (str): Detailed description of the data.
    """
    id: int
    code: str
    name: str
    type: str
    description: str
    value: str

    class Config:
        """Pydantic configuration for ORM model compatibility."""
        from_attributes = True
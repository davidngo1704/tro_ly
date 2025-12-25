"""Data database model.

Defines the SQLAlchemy ORM model for the Datas table.
"""

from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Data(Base):
    """Data database model.
    
    Represents a Data record in the database with code, name, type,
    and description fields.
    
    Attributes:
        id (int): Primary key and unique identifier.
        code (str): Data code identifier.
        name (str): Data name/title.
        type (str): Data type classification.
        description (str): Detailed description of the Data.
    """
    __tablename__ = "Datas"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    value = Column(String, nullable=False)


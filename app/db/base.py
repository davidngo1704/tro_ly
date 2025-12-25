"""Database base declarative module.

Defines the SQLAlchemy declarative base for all ORM models.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""SQLAlchemy declarative base for all ORM models."""
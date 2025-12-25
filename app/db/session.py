"""Database session module.

Provides database engine, session factory, and dependency injection
for database sessions throughout the application.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/data.db")
"""Database connection URL from environment or default SQLite."""

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
"""SQLAlchemy engine instance."""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""Session factory for creating database sessions."""

def get_db():
    """Dependency injection function for database sessions.
    
    Creates a new database session for each request and ensures
    proper cleanup even if an error occurs.
    
    Yields:
        Session: A new SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


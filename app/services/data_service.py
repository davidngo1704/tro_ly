"""data service module.

Provides the dataService class for managing datas in the database.
"""

from app.services.base_service import BaseService
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.session import get_db

from app.models.data_model import Data

class dataService(BaseService):
    """Service for managing data database operations.
    
    Extends BaseService to provide CRUD operations for data model.
    """
    model = Data

def get_data_service(db: Session = Depends(get_db)):
    """Dependency injection function for dataService.
    
    Args:
        db (Session): The database session.
        
    Returns:
        dataService: A new instance of dataService.
    """
    return dataService(db)

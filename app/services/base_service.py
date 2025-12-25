"""Base service module for database operations.

Provides the BaseService class with common CRUD operations for SQLAlchemy models.
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

class BaseService:
    """Base service class for database model operations.
    
    Provides common CRUD (Create, Read, Update, Delete) operations
    for SQLAlchemy models.
    """
    model = None  # Model SQLAlchemy, service con phải gán

    def __init__(self, db: Session):
        """Initialize the service with a database session.
        
        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def get_all(self):
        """Get all records of the model.
        
        Returns:
            list: All records from the database.
        """
        return self.db.query(self.model).all()

    def get_by_id(self, obj_id: int):
        """Get a record by its ID.
        
        Args:
            obj_id (int): The ID of the record.
            
        Returns:
            Model instance: The requested record.
            
        Raises:
            HTTPException: If the record is not found (404).
        """
        obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{self.model.__name__} not found")
        return obj

    def create(self, data):
        """Create a new record.
        
        Args:
            data: Pydantic schema with the data to create.
            
        Returns:
            Model instance: The created record.
        """
        obj = self.model(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj_id: int, data):
        """Update an existing record.
        
        Args:
            obj_id (int): The ID of the record to update.
            data: Pydantic schema with the updated data.
            
        Returns:
            Model instance: The updated record.
        """
        obj = self.get_by_id(obj_id)
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj_id: int):
        """Delete a record by ID.
        
        Args:
            obj_id (int): The ID of the record to delete.
            
        Returns:
            dict: Confirmation message.
        """
        obj = self.get_by_id(obj_id)
        self.db.delete(obj)
        self.db.commit()
        return {"message": f"{self.model.__name__} deleted"}

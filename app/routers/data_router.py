"""data router module.

Provides API endpoints for data management (CRUD operations).
"""

from fastapi import APIRouter, Depends
from typing import List

from app.schemas.data_schema import dataCreate, dataUpdate, dataResponse
from app.services.data_service import dataService, get_data_service


router = APIRouter()


@router.post("/", response_model=dataResponse)
def create_data(data: dataCreate, service: dataService = Depends(get_data_service)):
    """Create a new data.
    
    Args:
        data (dataCreate): The data data to create.
        service (dataService): The data service instance.
    
    Returns:
        dataResponse: The created data.
    """
    return service.create(data)


@router.get("/", response_model=List[dataResponse])
def list_data(service: dataService = Depends(get_data_service)):
    """Get all datas.
    
    Args:
        service (dataService): The data service instance.
    
    Returns:
        List[dataResponse]: List of all datas.
    """
    return service.get_all()


@router.get("/{data_id}", response_model=dataResponse)
def get_data(data_id: int, service: dataService = Depends(get_data_service)):
    """Get a specific data by ID.
    
    Args:
        data_id (int): The data ID.
        service (dataService): The data service instance.
    
    Returns:
        dataResponse: The requested data.
    """
    return service.get_by_id(data_id)


@router.put("/{data_id}", response_model=dataResponse)
def update_data(
    data_id: int,
    data: dataUpdate,
    service: dataService = Depends(get_data_service)
):
    """Update an existing data.
    
    Args:
        data_id (int): The data ID to update.
        data (dataUpdate): The updated data data.
        service (dataService): The data service instance.
    
    Returns:
        dataResponse: The updated data.
    """
    return service.update(data_id, data)


@router.delete("/{data_id}")
def delete_data(data_id: int, service: dataUpdate = Depends(get_data_service)):
    """Delete a data by ID.
    
    Args:
        data_id (int): The data ID to delete.
        service (dataService): The data service instance.
    
    Returns:
        Response indicating deletion success.
    """
    return service.delete(data_id)

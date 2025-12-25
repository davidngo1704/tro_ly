"""Main FastAPI application module.

This module initializes the FastAPI application with CORS middleware and includes
routers for chat and notification endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.routers import data_router, chat_router

app = FastAPI(title="Trợ Lý")
"""FastAPI application instance configured with title 'Thành Đại' (Danh)."""

Base.metadata.create_all(bind=engine)

# Configure CORS middleware to allow all origins and methods for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,  # Credentials not required
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(data_router.router, prefix="/data", tags=["data"])

app.include_router(chat_router.router, prefix="/chat", tags=["chat"])
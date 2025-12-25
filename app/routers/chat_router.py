"""Chat router module.

Provides API endpoints for chat interactions including REST and WebSocket endpoints.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from app.schemas.common_schema import ChatModel

router = APIRouter()

@router.post("/")
async def chat(data: ChatModel):
    """Process a chat message from a user or agent.
    
    Args:
        data (ChatModel): The chat request containing message and agent identifier.
    
    Returns:
        dict: Response with reply message.
    """

    reply_text = f"đã nhận: {data.message}"

    return {
        "reply": reply_text
    }
    
    

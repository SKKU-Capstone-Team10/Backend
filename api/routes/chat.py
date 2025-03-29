from typing import Any

from fastapi import APIRouter, HTTPException

from core.db import SessionDep

from models import Chat
from schemas.chat import (
    ChatCreate,
    ChatHistoryResponse,
    ChatResponse
)

router = APIRouter(prefix="/chat", tags=['Chat'])

# Initial chat -> Create a new Chat Session
@router.post('/', response_model=ChatResponse)
def create_chat(db: SessionDep, req: ChatCreate) -> Any:
    # Pass chat content to AI server
    if req.session_id == None:
        # Create a new chat session
        pass
    else:
        # Add requested content to the chat session
        pass
    # Response the message from AI server
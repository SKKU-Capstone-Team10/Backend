from typing import Any

from fastapi import APIRouter, HTTPException

from core.auth import CurrentUser

from models import (
    ChatSession
)
from schemas.chat_session import (
    ChatSessionUpdateTitle
)
from schemas.message import Message
from crud.chat_session import (
    update_session_title
)

router = APIRouter(prefix='/chat-session', tags=['Chat Session'])

# Chat Sessions are created by /api/chat/initial

# Fetch Chat Sessions belong to a user
@router.get('/{id}')
def fetch_chat_sessions(id: str):
    return "tmp"

# Rename a Chat Session
@router.patch('/update/title', response_model=Message)
def update_chat_session(id: str, req: ChatSessionUpdateTitle):
    return "tmp"

# Delete a Chat Session
@router.delete('/{id}', response_model=Message)
def delete_chat_session(id: str, current_user: CurrentUser) -> Any:
    return "tmp"

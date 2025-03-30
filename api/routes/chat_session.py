from uuid import UUID
from typing import Any

from fastapi import APIRouter, HTTPException

from core.auth import CurrentUser
from core.db import SessionDep

from models import (
    ChatSession
)
from schemas.chat_session import (
    ChatSessionList,
    ChatSessionUpdateTitle
)
from schemas.message import Message
from crud.chat_session import (
    update_session_title,
    read_sessions
)

router = APIRouter(prefix='/chat-session', tags=['Chat Session'])

# Chat Sessions are created by /api/chat/initial

# Fetch Chat Sessions belong to a user
@router.get('/{user_id}', response_model=ChatSessionList)
def fetch_chat_sessions(db: SessionDep, user_id: UUID, current_user: CurrentUser) -> Any:
    session_list = read_sessions(db, user_id)
    res_data = ChatSessionList(
        user_id=user_id,
        session_list=session_list
    )
    return res_data

# Rename a Chat Session
@router.patch('/update/title', response_model=Message)
def update_chat_session_title(db: SessionDep, id: UUID, req: ChatSessionUpdateTitle) -> Any:
    return "tmp"

# Delete a Chat Session
@router.delete('/{id}', response_model=Message)
def delete_chat_session(db: SessionDep, id: UUID, current_user: CurrentUser) -> Any:
    return Message(message="tmp")

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
    ChatSessionUpdateTitle,
    ChatSessionDelete
)
from schemas.message import Message
from crud.chat_session import (
    update_session_title,
    get_session_by_id,
    read_sessions,
    delete_session
)

router = APIRouter(prefix='/chat-session', tags=['Chat Session'])

# Chat Sessions are created by /api/chat/initial

# Fetch Chat Sessions belong to a user
@router.get('/{user_id}', response_model=ChatSessionList)
def fetch_chat_sessions(db: SessionDep, user_id: UUID, current_user: CurrentUser) -> Any:
    session_list = read_sessions(db, user_id)
    res_data = ChatSessionList(
        user_id=user_id,
        chat_sessions=session_list
    )
    return res_data

# Rename a Chat Session
@router.patch('/update/title', response_model=Message)
def update_chat_session_title(db: SessionDep, req: ChatSessionUpdateTitle) -> Any:
    return "tmp"

# Delete a Chat Session
@router.delete('/{id}', response_model=Message)
def delete_chat_session(db: SessionDep, current_user: CurrentUser, id: UUID) -> Any:
    session = get_session_by_id(db, id)

    if not session:
        raise HTTPException(status_code=404, detail="Chat Session not found")
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Users can delete only their chat sessions."
        )
    
    delete_session(db, session) # Cascade delete chat

    return Message(message="Chat Session deleted successfully")

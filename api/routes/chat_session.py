from uuid import UUID
from typing import Any

from fastapi import APIRouter, HTTPException

from core.auth import CurrentUser
from core.db import SessionDep, UuidDep

from models import (
    ChatSession
)
from schemas.chat_session import (
    ChatSessionList,
    ChatSessionUpdateTitle
)
from schemas.message import Message
from crud.chat_session import (
    patch_session_title,
    get_session_by_id,
    read_sessions,
    delete_session
)

router = APIRouter(prefix='/chat-session', tags=['Chat Session'])

# Chat Sessions are created by /api/chat/initial

# Fetch Chat Sessions belong to a user
@router.get('/{user_id}', response_model=ChatSessionList)
def fetch_chat_sessions(db: SessionDep, user_id: UUID, current_user: CurrentUser) -> Any:
    """
    Fetch Chat Sessions of a user with the UUID\n
    Token Required. \n
    - **user_id**: User's UUID to fetch chat sessions \n
    403 Error - Invalid token. \n
    404 Error - User with the token not found.
    """
    session_list = read_sessions(db, user_id)
    res_data = ChatSessionList(
        user_id=user_id,
        chat_sessions=session_list
    )
    return res_data

# Rename a Chat Session
@router.patch('/update/title', response_model=Message)
def update_chat_session_title(db: SessionDep, req: ChatSessionUpdateTitle) -> Any:
    """
    Update the tile of chat session\n
    **NOT Implemented yet**
    """
    session = get_session_by_id(db, req.id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat Session not found")

    success = patch_session_title(db, session, req.new_title)
    if not success: # Failed to write in DB
        raise HTTPException(status_code=500, detail="Title update failed. Check server log.")
    
    return Message(message="Updated successfully.")

# Delete a Chat Session
@router.delete('/{id}', response_model=Message)
def delete_chat_session(db: SessionDep, current_user: CurrentUser, id: UuidDep) -> Any:
    """
    Delete a chat session. \n
    Token Required. \n
    Cascade delete chats belong to it.
    - **id**: uuid of chat session to delete \n
    403 Error - Invalid token. Or owner of the session and token do not match \n
    404 Error - User with the token not found. Or Chat Session with the UUID not found.
    500 Error = DB failure, Server's fault
    """
    session = get_session_by_id(db, id)

    if not session:
        raise HTTPException(status_code=404, detail="Chat Session not found")
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Users can delete only their chat sessions."
        )
    
    success = delete_session(db, session) # Cascade delete chat
    if not success:
        raise HTTPException(status_code=500, detail="Delete failed")

    return Message(message="Chat Session deleted successfully")

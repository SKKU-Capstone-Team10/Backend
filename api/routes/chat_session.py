from fastapi import APIRouter, HTTPException

from models import (
    ChatSession
)

router = APIRouter(prefix='/chat-session', tags=['Chat Session'])

# Chat Sessions are created by /api/chat/initial

# Fetch Chat Sessions belong to a user
@router.get('/{id}')
def fetch_chat_sessions(id: str):
    return "tmp"

# Fetch Chats belong to a Chat Session
@router.get('/{id}')
def fetch_chats(id: str):
    return "tmp"

# Rename a Chat Session
@router.patch('/{id}')
def update_chat_session(id: str):
    return "tmp"

# Delete a Chat Session
@router.delete('/{id}')
def delete_chat_session(id: str):
    return "tmp"

from typing import Any
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException

from core.db import SessionDep
from core.auth import CurrentUser

from models import Chat
from schemas.chat import (
    ChatCreate,
    ChatHistoryResponse,
    ChatResponse
)

from crud.chat_session import create_session
from crud.chat import create_chat

router = APIRouter(prefix="/chat", tags=['Chat'])
executor = ThreadPoolExecutor()

# Initial chat -> Create a new Chat Session
@router.post('/', response_model=ChatResponse)
def post_chat(db: SessionDep, req: ChatCreate, current_user: CurrentUser) -> Any:
    req_data = req.model_dump(exclude_unset=True) # Pydantic.BaseModel -> python.dict
    
    # Request a reply to ai server
    future = executor.submit(lambda _: "AI Reply", req_data['content'])

    # Check if Session is exist
    if 'session_id' not in req_data.keys():
        req_data['session_id'] = create_session(db, current_user.id)
    
    # Record user's chat
    _ = create_chat(db, ChatCreate(**req_data))

    # Wait for ai server's response
    ai_reply = future.result()
    # Response the message from AI server
    ai_chat = ChatCreate(
        session_id=req_data['session_id'],
        sender="host",
        content=ai_reply
    )
    ai_chat_recorded = create_chat(db, ai_chat)
    return ChatResponse.model_validate(ai_chat_recorded)

# Fetch Chats belong to a Chat Session
@router.get('/{id}', response_model=ChatHistoryResponse)
def fetch_chats(id: str, current_user: CurrentUser) -> Any:
    return "tmp"
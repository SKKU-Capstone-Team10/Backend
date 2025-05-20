from uuid import UUID
from typing import Any
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, HTTPException

from core.db import SessionDep
from core.auth import CurrentUser
from core.config import settings

from models import Chat
from schemas.chat import (
    ChatCreate,
    ChatHistoryResponse,
    ChatResponse
)

from crud.chat_session import create_session
from crud.chat import (
    create_chat,
    read_chats
)

from api.functions.rag import get_ai_reply

router = APIRouter(prefix="/chat", tags=['Chat'])
executor = ThreadPoolExecutor()

# Initial chat -> Create a new Chat Session
@router.post('/', response_model=ChatResponse,
            summary="Send Chat & Get AI response. Optional[Create New Chat Session]")
def post_chat(db: SessionDep, req: ChatCreate, current_user: CurrentUser) -> Any:
    """
    Add new chat from user and get AI's response message. \n
    Token Required \n
    - **session_id** Optional: Chat Session to add the chats both from user and AI. Remain **None** to create new chat session.
    - **sender**: Enum type[user/host], Request it with 'user', Response filled with 'host'
    - **content**: chat content from user \n
    403 Error - Invalid token. \n
    404 Error - User with the token not found.
    """
    req_data = req.model_dump(exclude_unset=True) # Pydantic.BaseModel -> python.dict
    
    # Check if Session is exist -> not exist means first chat
    is_first_chat = 'session_id' not in req_data.keys()

    # Request a reply to ai server
    res_rag = get_ai_reply(req_data['content'], is_first_chat)
    res_content = res_rag['content']
    res_ticker = res_rag['ticker']

    # If first chat, create a Chat Session
    if is_first_chat == True:
        res_title = res_rag['title']
        req_data['session_id'] = create_session(db, current_user.id, res_title)
    
    # Record user's chat
    _ = create_chat(db, ChatCreate(**req_data))

    # Response the message from AI server
    ai_chat = ChatCreate(
        session_id=req_data['session_id'],
        sender="host",
        content=res_content,
        ticker=res_ticker
    )
    res = create_chat(db, ai_chat).model_dump()
    if is_first_chat == True:
        res['title'] = res_title

    return ChatResponse(**res)

# Fetch Chats belong to a Chat Session
@router.get('/{session_id}', response_model=ChatHistoryResponse)
def fetch_chats(db: SessionDep, session_id: UUID, current_user: CurrentUser) -> Any:
    """
    Fetch chats of a session by uuid of the chat session. \n
    Token Required. \n
    - **session_id**: uuid of the chat session \n
    403 Error - Invalid token. \n
    404 Error - User with the token not found.
    """
    chat_list = read_chats(db, session_id)
    res_data = ChatHistoryResponse(
        session_id=session_id,
        chats=chat_list
    )
    return res_data
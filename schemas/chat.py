from uuid import UUID
from typing import Optional, Literal, List
from datetime import datetime
from pydantic import BaseModel

# Request Field
class ChatCreate(BaseModel):
    session_id: Optional[UUID] = None # None indicates to create new chat session
    sender: Literal["user", "host"]
    content: str
    ticker: Optional[str] = None
    
# Response Field for individual chat (with refs for AI responses)
class ChatResponse(BaseModel):
    id: UUID
    session_id: UUID
    sender: Literal["user", "host"]
    title: Optional[str] = None
    content: str
    ticker: Optional[str] = None
    refs: Optional[List[str]] = None
    created_at: datetime
    class Config():
        from_attributes = True

# Response Field for chat history (without refs)
class ChatHistoryItem(BaseModel):
    id: UUID
    session_id: UUID
    sender: Literal["user", "host"]
    content: str
    ticker: Optional[str] = None
    created_at: datetime
    class Config():
        from_attributes = True

# Response Field for fetching a Chat Session History
class ChatHistoryResponse(BaseModel):
    session_id: UUID
    chats: List[ChatHistoryItem]
from uuid import UUID
from typing import List
from pydantic import BaseModel

from models import ChatSession

class ChatSessionList(BaseModel):
    user_id: UUID
    chat_sessions: List[ChatSession]

class ChatSessionUpdateTitle(BaseModel):
    id: UUID
    new_title: str

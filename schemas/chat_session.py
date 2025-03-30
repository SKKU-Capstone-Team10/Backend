from uuid import UUID
from pydantic import BaseModel

class ChatSessionUpdateTitle(BaseModel):
    id: UUID
    title: str

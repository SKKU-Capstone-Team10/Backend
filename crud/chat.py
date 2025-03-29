from uuid import UUID, uuid4
from typing import Dict

from sqlmodel import Session

from models import Chat
from schemas.chat import ChatCreate

def create_chat(db: Session, req: ChatCreate) -> Chat:
    # Create a new Chat entity
    new_chat = Chat(
        session_id=req.session_id,
        sender=req.sender,
        content=req.content
    )

    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat
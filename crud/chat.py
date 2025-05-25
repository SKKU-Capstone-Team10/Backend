from uuid import UUID, uuid4
from typing import List

from sqlmodel import Session, select

from models import Chat
from schemas.chat import ChatCreate

def create_chat(db: Session, req: ChatCreate) -> Chat:
    # Create a new Chat entity
    new_chat = Chat(
        session_id=req.session_id,
        sender=req.sender,
        content=req.content,
        ticker=req.ticker or ""
    )

    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat

def read_chats(db: Session, session_id: UUID) -> List[Chat]:
    statement = select(Chat).where(Chat.session_id == session_id)
    chat_list = db.exec(statement)
    return chat_list
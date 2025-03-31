from uuid import UUID
from typing import List
from sqlmodel import Session, select

from models import ChatSession
from schemas.chat_session import ChatSessionList

def create_session(db: Session, user_id: UUID) -> UUID:
    new_session = ChatSession(
        user_id=user_id,
        title='dummy'
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session.id

def get_session_by_id(db: Session, id: UUID) -> ChatSession:
    statement = select(ChatSession).where(ChatSession.id == id)
    session = db.exec(statement)
    return session

def read_sessions(db: Session, user_id: UUID) -> List[ChatSession]:
    statement = select(ChatSession).where(ChatSession.user_id == user_id)
    session_list = db.exec(statement)
    return session_list

def update_session_title(db: Session, id: UUID, new_title: str) -> None:
    pass

def delete_session(db: Session, session: ChatSession) -> None:
    db.delete(session)
    db.commit()
    return None
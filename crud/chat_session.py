from uuid import UUID
from typing import List
from sqlmodel import Session, select

from fastapi import HTTPException

from models import ChatSession
from schemas.chat_session import ChatSessionList

def create_session(db: Session, user_id: UUID, title: str) -> UUID:
    new_session = ChatSession(
        user_id=user_id,
        title=title
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session.id

def get_session_by_id(db: Session, id: UUID) -> ChatSession:
    session = db.get(ChatSession, id)
    return session

def read_sessions(db: Session, user_id: UUID) -> List[ChatSession]:
    statement = select(ChatSession).where(ChatSession.user_id == user_id)
    session_list = db.exec(statement)
    return list(session_list)

def patch_session_title(db: Session, session: ChatSession, new_title: str) -> None:
    try:
        session.title = new_title
        db.add(session)
        db.commit()
        db.refresh(session)
        return True
    except Exception as e:
        db.rollback()
        print(f"[patch_session_title] ERROR: {e}")
        return False

def delete_session(db: Session, session: ChatSession) -> bool:
    try:
        db.delete(session)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[delete_session] ERROR: {e}")
        return False
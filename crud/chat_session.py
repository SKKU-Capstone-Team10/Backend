from uuid import UUID
from typing import List
from sqlmodel import Session

from models import ChatSession

def create_session(db: Session, user_id: UUID) -> ChatSession:
    pass

def read_sessions(db: Session, user_id: UUID) -> List[ChatSession]:
    pass

def update_session_title(db: Session, id: UUID, new_title: str) -> None:
    pass

def delete_session(db: Session, session_id: UUID) -> None:
    pass
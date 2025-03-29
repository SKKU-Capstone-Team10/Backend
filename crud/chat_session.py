from uuid import UUID
from sqlmodel import Session

def create_session(db: Session, user_id: UUID) -> UUID:
    pass
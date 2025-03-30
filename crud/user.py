from uuid import UUID
from sqlmodel import Session, select

from core.auth import get_password_hash

from models import User
from schemas.user import UserCreate, UserPublic


def create_user(db: Session, req: UserCreate) -> UserPublic:
    new_user = User(
        email = req.email,
        username = req.username,
        password = get_password_hash(req.password1)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email:str) -> User | None:
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    return user

def get_user_by_id(db: Session, id: UUID) -> User | None:
    user = db.get(User, id)
    return user

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
    return None
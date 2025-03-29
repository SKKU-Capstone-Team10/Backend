from sqlmodel import Session

from core.auth import verify_password
from crud.user import get_user_by_email

from models import User

def authenticate(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user